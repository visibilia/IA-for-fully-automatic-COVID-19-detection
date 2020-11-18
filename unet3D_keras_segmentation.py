 """ 
    This piece of source code is part of FADCIL project from Visibilia
    More details about this project at: http://visibilia.net.br/fadcil
    Last updated: 11/17/2020
 """


from tensorflow.keras import Model
from tensorflow.keras.layers import Input, BatchNormalization, Conv3D, Concatenate, Cropping3D, UpSampling3D, Dropout, Add, \
    Multiply, Lambda, ZeroPadding3D, SpatialDropout3D, Flatten, Dense, Activation, Conv3DTranspose
from tensorflow.keras import regularizers
from tensorflow.keras.layers import MaxPooling3D
from tensorflow.keras import optimizers
from keras.utils import plot_model
from tensorflow.keras.activations import softmax, sigmoid
import numpy as np
from keras import backend as K
import config as gdrive
from model.helper_classes import Optimizers
from model.helper_classes import Winit
from model.helper_classes import LossName
from model.helper_classes import FActivation
import tensorflow as tf
import tensorflow_addons as tfa
tf.keras.backend.set_image_data_format('channels_first')
from model.segm3d import Segm3D


def unet_cropping(first_block=None, net=None):
    """ Crops feature maps of different size, it keeps the center of both feature maps
    """
    net_shape = (int(net.shape[2]), int(net.shape[3]), int(net.shape[4]))
    first_block_shape = (int(first_block.shape[2]), int(first_block.shape[3]), int(first_block.shape[4]))
    cropping = tuple(np.asarray(first_block_shape) - np.asarray(net_shape))
    first_block = Cropping3D(cropping=((int(cropping[0] / 2), int(cropping[0] / 2)),
                                       (int(cropping[1] / 2), int(cropping[1] / 2)),
                                       (int(cropping[2] / 2), int(cropping[2] / 2))))(first_block)
    
    return first_block


class UNet3DModel(Segm3D):
    """ 3D U-Net network architecture.
        It trains patches of 132x132x132 of the CT scan to produce an output of 44x44x44
        Simmilarly, 108x108x108 patch produces output of 20x20x20
        This implementation has the same field of view proposed by 3D U-Net (88)
    """
    def down_path(self, tensor_in, nfilters, nonlinearity, initializer, do_bn, name_bottom=None):
        """ Down path of the 3D U-Net
        """
        kernel_regularizer = None if not self.do_l2 else regularizers.l2(0.00003)
        if not do_bn:
            conv1 = Conv3D(nfilters, (3, 3, 3), activation=nonlinearity, padding='valid',
                           kernel_initializer=initializer, kernel_regularizer=kernel_regularizer)(tensor_in)
            conv1 = Conv3D(nfilters * 2, (3, 3, 3), activation=nonlinearity, padding='valid',
                           kernel_initializer=initializer, name=name_bottom)(conv1)
        else:
            conv1 = Conv3D(nfilters, (3, 3, 3), activation=None, padding='valid',
                           kernel_initializer=initializer, kernel_regularizer=kernel_regularizer)(tensor_in)


            conv1 = tfa.layers.InstanceNormalization(axis=1, center=True, scale=True)(conv1)
            # conv1 = BatchNormalization(axis=1, epsilon=1e-5, momentum=0.999)(conv1)
            conv1 = Activation(activation=nonlinearity)(conv1)
            conv1 = Conv3D(nfilters * 2, (3, 3, 3), activation=None, padding='valid', kernel_initializer=initializer,
                           name=name_bottom)(conv1)
            conv1 = tfa.layers.InstanceNormalization(axis=1, center=True, scale=True)(conv1)
            # conv1 = BatchNormalization(axis=1, epsilon=1e-5, momentum=0.999)(conv1)
            conv1 = Activation(activation=nonlinearity)(conv1)
        
        return conv1
    
    def up_path(self, tensor_in, nfilters, nonlinearity, initializer, do_bn):
        """ Up path of the 3D U-Net
        """
        kernel_regularizer = None if not self.do_l2 else regularizers.l2(0.00003)
        if not do_bn:
            conv5 = Conv3D(nfilters, (3, 3, 3), activation=nonlinearity, padding='valid',
                           kernel_initializer=initializer, kernel_regularizer=kernel_regularizer)(tensor_in)
            conv5 = Conv3D(nfilters, (3, 3, 3), activation=nonlinearity, padding='valid',
                           kernel_initializer=initializer)(conv5)
        else:
            conv5 = Conv3D(nfilters, (3, 3, 3), activation=None, padding='valid',
                           kernel_initializer=initializer, kernel_regularizer=kernel_regularizer)(tensor_in)
            conv5 = tfa.layers.InstanceNormalization(axis=1, center=True, scale=True)(conv5)
            #conv5 = BatchNormalization(axis=1, epsilon=1e-5, momentum=0.999)(conv5)
            conv5 = Activation(activation=nonlinearity)(conv5)
            conv5 = Conv3D(nfilters, (3, 3, 3), activation=None, padding='valid', kernel_initializer=initializer)(conv5)
            conv5 = tfa.layers.InstanceNormalization(axis=1, center=True, scale=True)(conv5)
            #conv5 = BatchNormalization(axis=1, epsilon=1e-5, momentum=0.999)(conv5)
            conv5 = Activation(activation=nonlinearity)(conv5)

        return conv5


    @staticmethod
    def concat_up_deconv(tensor_up, tensor_crop, do_dropout=False, num_filters=1):
        """ Concatenates the transposed 3D convolution (better than upsampling) of the feature maps
        """
        up5 = Conv3DTranspose(filters=tensor_up.shape[1], kernel_size=(3, 3, 3), strides=(2, 2, 2), padding='same',
                              data_format='channels_first', activation='relu')(tensor_up)
        conv3_cropped = unet_cropping(first_block=tensor_crop, net=up5)

        if do_dropout:
            conv3_cropped = SpatialDropout3D(rate=0.2)(conv3_cropped)

        up5 = Concatenate(axis=1)([up5, conv3_cropped])

        return up5


    def build_UNetCicek_deconv(self, nonlinearity, num_classes=2, do_dropout=False, do_bn=False, nfilters=32,
                        initializer=Winit.GLOROTUNI, activation=softmax_axis1):
        """ This Model reproduces baseline 3D U-Net Cicek with transposed 3D convolutions
            https://arxiv.org/abs/1606.06650
        """
        conv1 = self.down_path(self.inputs, nfilters, nonlinearity, initializer, do_bn)
        pool1 = MaxPooling3D(pool_size=self.pool_size)(conv1)

        conv2 = self.down_path(pool1, nfilters * 2, nonlinearity, initializer, do_bn)
        pool2 = MaxPooling3D(pool_size=self.pool_size)(conv2)

        conv3 = self.down_path(pool2, nfilters * 4, nonlinearity, initializer, do_bn)
        pool3 = MaxPooling3D(pool_size=self.pool_size)(conv3)

        conv4 = self.down_path(pool3, nfilters * 8, nonlinearity, initializer, do_bn)

        up5 = self.concat_up_deconv(conv4, conv3, do_dropout)
        conv5 = self.up_path(up5, nfilters * 8, nonlinearity, initializer, do_bn)

        up6 = self.concat_up_deconv(conv5, conv2, do_dropout)
        conv6 = self.up_path(up6, nfilters * 4, nonlinearity, initializer, do_bn)

        up7 = self.concat_up_deconv(conv6, conv1, do_dropout)
        conv7 = self.up_path(up7, nfilters * 2, nonlinearity, initializer, do_bn)

        output = Conv3D(num_classes, (1, 1, 1), activation=activation, padding='valid',
                        kernel_initializer=initializer, name='output_segm')(conv7)
        self.model_segm = Model(inputs=self.inputs, outputs=output)
        self.dl_network_name = 'build_UNetCicek_deconv'

        return output


        
    def __init__(self):
        """ Initilizes the variables for the 3D U-Net
        """
        self.inputs = None
        self.pool_size = (2, 2, 2)


