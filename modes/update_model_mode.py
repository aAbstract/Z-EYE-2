import PCA.PCA_math as PCA
import settings.settings as set_man
import utils.log as log_man


def update_model_mode_setup():
    pass


def update_model_mode_loop():
    # train the model
    log_man.add_log('modes.training_mode_loop',
                    'INFO', f"fitting PCA model to the dataset")
    PCA.train_model()
    log_man.add_log('modes.training_mode_loop',
                    'INFO', f"done fitting PCA model to the dataset")

    set_man.save_settings()

    return -1
