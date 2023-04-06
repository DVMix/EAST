import os
import shutil
from pyicdartools import TL_iou, rrc_evaluation_funcs


def compute_hmean(submit_file_path):
    print('EAST <==> Evaluation <==> Compute Hmean <==> Begin')

    basename = os.path.basename(submit_file_path)
    assert basename == 'submit.zip', 'There is no submit.zip'

    dir_name = os.path.dirname(submit_file_path)
    gt_file_path = os.path.join(dir_name, 'gt.zip')
    assert os.path.isfile(gt_file_path), 'There is no gt.zip'

    log_file_path = os.path.join(dir_name, 'log_epoch_hmean.txt')
    if not os.path.isfile(log_file_path):
        os.mknod(log_file_path)

    result_dir_path = os.path.join(dir_name, 'result')
    try:
        shutil.rmtree(result_dir_path)
    except:
        pass
    os.mkdir(result_dir_path)

    res_dict = rrc_evaluation_funcs.main_evaluation(
        {'g': gt_file_path, 's': submit_file_path, 'o': result_dir_path},
        TL_iou.default_evaluation_params, TL_iou.validate_data,
        TL_iou.evaluate_method
    )

    print(res_dict)
    recall = res_dict['method']['recall']

    precision = res_dict['method']['precision']

    hmean = res_dict['method']['hmean']

    print('EAST <==> Evaluation <==> Precision:{:.2f} Recall:{:.2f} Hmean{:.2f} <==> Done'.format(precision, recall,
                                                                                                  hmean))

    with open(log_file_path, 'a') as f:
        f.write(
            'EAST <==> Evaluation <==> Precision:{:.2f} Recall:{:.2f} Hmean{:.2f} <==> Done\n'.format(precision, recall,
                                                                                                      hmean))

    return hmean


if __name__ == '__main__':
    submit_file_path = '/home/djsong/update/result/submit.zip'
    h_mean = compute_hmean(submit_file_path)
