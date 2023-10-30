import tensorflow as tf

def efficientnet_v2l_model(
    input_shape,
    n_classes, 
    dense_nodes=1024, 
    conv_dropout=0.25, 
    dense_dropout=0.5,  
    output_activation='linear',
    model_name='efficientnet_v2l',
    train_base=False,
    **kwargs 
):

    """
    This function returns a efficientnet_v2l transfer learning model
    
    Arguments:
        input_shape: shape of the training data (row, column, channel)
        n_classes: number of output classes
        dense_nodes: number of nodes for the dense layer
        conv_dropout: dropout rate after the global pooling layer 
        dense_dropout: dropout rate after the dense layer
        output_activation: allows reuse for classification models
        model_name: unique name for model
        train_base: train the transfer model layers or not (True/False)
    
    Note:
        For EfficientNetV2, by default input preprocessing is included 
        as a part of the model (as a Rescaling layer), and thus 
        tf.keras.applications.efficientnet_v2.preprocess_input is actually 
        a pass-through function. In this use case, EfficientNetV2 models 
        expect their inputs to be float tensors of pixels with values in 
        the [0-255] range. At the same time, preprocessing as a part of 
        the model (i.e. Rescaling layer) can be disabled by setting 
        include_preprocessing argument to False. With preprocessing disabled 
        EfficientNetV2 models expect their inputs to be float tensors of 
        pixels with values in the [-1, 1] range.

    """

    # Load a pretrained model from keras.applications
    tranfer_model_base = tf.keras.applications.efficientnet_v2.EfficientNetV2L(
        input_shape=input_shape, 
        weights="imagenet", 
        include_top=False,
        include_preprocessing=False # Images already scaled to [0., 1.]
    )

    # Freeze the mobileNet model layers
    tranfer_model_base.trainable = train_base

    # Build model
    inputs = tf.keras.Input(shape=input_shape)
    x = tf.keras.layers.Rescaling(scale=2., offset=-1.)(inputs) # Reset range to [-1., 1.]
    x = tranfer_model_base(x, training=False)
    x = tf.keras.layers.GlobalAveragePooling2D()(x)
    x = tf.keras.layers.Dropout(conv_dropout)(x)
    x = tf.keras.layers.Dense(
            units=dense_nodes,
            activation="relu",
        )(x)
    x = tf.keras.layers.Dropout(dense_dropout)(x)
    outputs = tf.keras.layers.Dense(
            units=n_classes,
            activation=output_activation,
        )(x)
    
    return tf.keras.Model(inputs, outputs, name=model_name)