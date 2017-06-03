# coding: utf-8

import operator
from os import listdir

from numpy import zeros, tile

TRAINING_PATH = 'digits/trainingDigits/'
TRAINING_REAL_NUMS = []
TEST_PATH = 'digits/testDigits/'
TEST_REAL_NUMS = []


def _make_matrix_by_file(file):
    """
    把指定文件内的数据生成一个一维矩阵
    :param file:
    :return:
    """
    file_data_array = zeros((1, 1024))  # 创建一个只有一行且存储文件所有数据的矩阵
    with open(file) as lines:
        # 把文件的所有数据存储在矩阵中
        for line_num, line in enumerate(lines):
            for i in range(32):
                file_data_array[0, 32 * line_num + i] = int(line[i])
    return file_data_array


def generate_training_matrix():
    """
    读取训练文件的数据并且转化为一个矩阵
    :return:
    """
    training_file_list = listdir(TRAINING_PATH)  # 获取训练文件列表
    training_matrix = zeros((len(training_file_list), 1024))  # 创建一个矩阵，行数为训练文件数，列数为每个训练文件的字符数
    for file_index, training_file in enumerate(training_file_list):
        TRAINING_REAL_NUMS.append(training_file.split('.')[0].split('_')[0])  # 把正确的数字保存在列表中
        # 把所有的训练文件数据存储在一个矩阵中
        training_matrix[file_index, :] = _make_matrix_by_file(TRAINING_PATH + training_file)
    return training_matrix


def generate_test_matrix_list():
    test_file_list = listdir(TEST_PATH)  # 获取测试文件列表
    test_matrix1_list = []
    for test_file in test_file_list:
        TEST_REAL_NUMS.append(test_file.split('.')[0].split('_')[0])
        # 把所有的测试文件矩阵保存为一个list
        test_matrix1_list.append(_make_matrix_by_file(TEST_PATH + test_file))
    return test_matrix1_list


def classify(training_matrix, test_matrix, k):
    training_matrix_lines = training_matrix.shape[0]  # 训练矩阵的总行数，也就是训练文件数
    test_matrix = tile(test_matrix, (training_matrix_lines, 1))  # 对测试矩阵进行行复制，使其行数和训练矩阵行数一样多
    distances = (((test_matrix - training_matrix) ** 2).sum(axis=1)) ** 0.5  # 获取测试数据和所有的训练数据的差异值list
    sortedDistances = distances.argsort()  # 对差异值按从小到大进行排序

    classCount = {}

    for i in range(k):
        voteIlabel = TRAINING_REAL_NUMS[sortedDistances[i]]
        classCount[voteIlabel] = classCount.get(voteIlabel, 0) + 1

    # 对类别出现的频次进行排序，从高到低
    sortedClassCount = sorted(classCount.items(), key=operator.itemgetter(1), reverse=True)

    # 返回出现频次最高的类别
    return sortedClassCount[0][0]


def main():
    training_matrix = generate_training_matrix()
    test_matrix_list = generate_test_matrix_list()
    right = 0  # 正确的个数
    total = 0  # 总个数
    for idx, test_matrix in enumerate(test_matrix_list):
        real = TEST_REAL_NUMS[idx]
        guess = classify(training_matrix, test_matrix, 3)
        if real == guess:
            right += 1
        total += 1
        print('真实：', real, '，猜测：', guess)

    fail = total - right
    print(fail, '次失败，失败率', fail / total)


if __name__ == '__main__':
    main()
