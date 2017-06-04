# -*- coding: utf-8 -*-

import operator
from os import *

from PIL import Image
from numpy import zeros, tile, array

TRAINING_PATH = 'train_symbol/'
TRAINING_REAL_NUMS = []  # 训练数据的真实数字
TEST_PATH = 'symbol/'
TEST_REAL_NUMS = []  # 测试数据的真实数字


def _make_matrix_by_file(file):
    """
    把指定文件内的数据生成一个一维矩阵
    :param file:
    :return:
    """
    file_data_array = zeros((1, 90))  # 创建一个只有一行且存储文件所有数据的矩阵
    matrix = array(Image.open(file))
    # print(matrix.tolist())
    for i in range(10):
        for j in range(9):
            file_data_array[0, i * 9 + j] = 0 if matrix[j][i] else 1
    # print(file_data_array.tolist())
    return file_data_array


def generate_training_matrix():
    """
    读取所有训练文件的数据并且转化为一个矩阵
    :return:
    """
    training_file_list = listdir(TRAINING_PATH)  # 获取训练文件列表
    training_matrix = zeros((len(training_file_list), 90))  # 创建一个矩阵，行数为训练文件数，列数为每个训练文件的字符数
    for file_index, training_file in enumerate(training_file_list):
        TRAINING_REAL_NUMS.append(training_file.split('.')[0].split('_')[0])  # 把正确的数字保存在列表中
        # 把所有的训练文件数据存储在一个矩阵中
        training_matrix[file_index, :] = _make_matrix_by_file(TRAINING_PATH + training_file)
    return training_matrix


def generate_test_matrix_list():
    """
    读取所有测试文件的数据并且转化为一个矩阵list
    :return:
    """
    test_file_list = listdir(TEST_PATH)  # 获取测试文件列表
    test_matrix1_list = []
    for test_file in test_file_list:
        # TEST_REAL_NUMS.append(test_file.split('.')[0].split('_')[1])
        # 把所有的测试文件矩阵保存为一个list
        test_matrix1_list.append(_make_matrix_by_file(TEST_PATH + test_file))
    return test_matrix1_list


def classify(training_matrix, test_matrix, k=3):
    """
    通过训练矩阵对测试数据进行数字判断
    :param training_matrix: 完整的训练矩阵
    :param test_matrix: 测试数据
    :param k: 取最相似的k个训练数据
    :return: 分类结果
    """
    training_matrix_lines = training_matrix.shape[0]  # 训练矩阵的总行数，也就是训练文件数
    test_matrix = tile(test_matrix, (training_matrix_lines, 1))  # 对测试矩阵进行行复制，使其行数和训练矩阵行数一样多
    distances = (((test_matrix - training_matrix) ** 2).sum(axis=1)) ** 0.5  # 获取测试数据和所有的训练数据的差异值list
    sorted_distances_index = distances.argsort()  # 对差异值按从小到大进行排序，把排序前list的下标作为新list的值组成一个列表

    num_count = {}  # 记录某个数字的出现次数

    for i in range(k):
        # 根据下标获取到训练数据中该条数据所对应的真实数字（至于最终选不选该数字依赖于其出现的频率）
        one_possible_number = TRAINING_REAL_NUMS[sorted_distances_index[i]]
        # 先获取该数字当前的出现次数（没有就为0），之后把当前次数加一作为新的出现次数
        num_count[one_possible_number] = num_count.get(one_possible_number, 0) + 1

    # 对数字出现的频次进行排序，从高到低
    sorted_num_count = sorted(num_count.items(), key=operator.itemgetter(1), reverse=True)

    # 返回出现频次最高的数字
    return sorted_num_count[0][0]


def test_symbol(test_file):
    training_matrix = generate_training_matrix()

    file_data_array = zeros((1, 90))  # 创建一个只有一行且存储文件所有数据的矩阵
    test_matrix = array(test_file)
    for i in range(10):
        for j in range(9):
            file_data_array[0, i * 9 + j] = 0 if test_matrix[j][i] else 1
    guess = classify(training_matrix, file_data_array, 3)
    return guess


def run():
    training_matrix = generate_training_matrix()
    print(training_matrix)
    test_matrix_list = generate_test_matrix_list()
    test_file_list = listdir(TEST_PATH)  # 获取测试文件列表
    right = 0  # 正确的个数
    total = 0  # 总个数
    for idx, test_matrix in enumerate(test_matrix_list):
        # real = TEST_REAL_NUMS[idx]
        guess = classify(training_matrix, test_matrix, 3)
        rename(TEST_PATH + test_file_list[idx], TEST_PATH + str(guess) + '_0' + str(idx) + '.png')

        # if real == guess:
        #     right += 1
        # total += 1
        # print('real: ', real, ', guess: ', guess)

    fail = total - right
    print(fail, ' fails, fail rate is ', fail / total)


if __name__ == '__main__':
    run()
