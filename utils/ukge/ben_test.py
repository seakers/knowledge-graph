"""
Current working directory: Project root dir

=== usage
python run/run.py -m DM --data cn15k --lr 0.01 --batch_size 300
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys
import time

if './src' not in sys.path:
    sys.path.append('./src')

if './' not in sys.path:
    sys.path.append('./')

import os
from os.path import join
from src.data import Data

from src.trainer import Trainer
from src.list import ModelList
from src.testers import UKGE_logi_Tester, UKGE_rect_Tester
import datetime

import argparse
from src import param

import matplotlib.pyplot as plt
import random
import numpy as np

parser = argparse.ArgumentParser()
# required
parser.add_argument('--data', type=str, default='ppi5k',
                    help="the dir path where you store data (train.tsv, val.tsv, test.tsv). Default: ppi5k")
# optional
parser.add_argument("--verbose", help="print detailed info for debugging",
                    action="store_true")
parser.add_argument('-m', '--model', type=str, default='rect', help="choose model ('logi' or 'rect'). default: rect")
parser.add_argument('-d', '--dim', type=int, default=128, help="set dimension. default: 128")
parser.add_argument('--epoch', type=int, default=100, help="set number of epochs. default: 100")
parser.add_argument('--lr', type=float, default=0.001, help="set learning rate. default: 0.001")
parser.add_argument('--batch_size', type=int, default=1024, help="set batch size. default: 1024")
parser.add_argument('--n_neg', type=int, default=10, help="Number of negative samples per (h,r,t). default: 10")
parser.add_argument('--save_freq', type=int, default=10,
                    help="how often (how many epochs) to run validation and save tf models. default: 10")
parser.add_argument('--models_dir', type=str, default='./trained_models',
                    help="the dir path where you store trained models. A new directory will be created inside it.")

# regularizer coefficient (lambda)
parser.add_argument('--reg_scale', type=float, default=0.0005,
                    help="The scale for regularizer (lambda). Default 0.0005")

args = parser.parse_args()

data_dir = join('./data', args.data)
file_train = join(data_dir, 'train.tsv')  # training data
file_val = join(data_dir, 'query.tsv')  # validation datan
file_psl = join(data_dir, 'softlogic.tsv')  # probabilistic soft logic
# file_psl = join(data_dir, 'train.tsv')  # probabilistic soft logic
print('file_psl: %s' % file_psl)
# file_psl = None
more_filt = [file_val, join(data_dir, 'test.tsv')]
print('Read train.tsv from', data_dir)

# load data
this_data = Data()
this_data.load_data(file_train=file_train, file_val=file_val, file_psl=file_psl)
validator = UKGE_rect_Tester()
model_dir = './trained_models/3D_CHESS/rect_1030/'
data_filename = 'data.bin'
model_filename = 'model.bin'
start = time.time()
validator.build_by_file('./data/3D_CHESS/query.tsv', model_dir, model_filename, data_filename)
end = time.time()
print(end-start)
scores = validator.get_val()
ground_truth = [1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0]
print(scores)
print(ground_truth)
threshold = 0.25
true_positive_count = 0
true_negative_count = 0
false_positive_count = 0
false_negative_count = 0

for i in range(len(scores)):
    if scores[i] > threshold and ground_truth[i] == 1:
        true_positive_count += 1
    elif scores[i] < threshold and ground_truth[i] == 0:
        true_negative_count += 1
    elif scores[i] > threshold and ground_truth[i] == 0:
        false_positive_count += 1
    else:
        false_negative_count += 1

precision = true_positive_count / (true_positive_count + false_positive_count)
recall = true_positive_count / (true_positive_count + false_negative_count)

f1 = 2*(precision*recall)/(precision+recall)

print("Precision: "+str(precision))
print("Recall: "+str(recall))
print("F1: "+str(f1))

# instrument_ids = [1461,204,204,742,742,742,742,742,1066,1066,48,48,1240,1220]
# parameter_ids = [958,999,1018,1018,978,999,979,958,979,978,978,1018,978,978]
# instrument_names = []
# parameter_names = []

instrument_names = []
parameter_names = []
instrument_ids = []
parameter_ids = []

prob_instrument_names = []
prob_parameter_names = []
prob_instrument_ids = []
prob_parameter_ids = []
prob_probs = []

with open("/home/ben/repos/UKGE/KG raw data/prob_kg.csv", "r") as kg_file:
    next(kg_file)
    for line in kg_file.readlines():
        line.rstrip()
        tokens = line.split(",")
        if tokens[1] == "OBSERVES":
            instrument_names.append(tokens[0])
            parameter_names.append(tokens[2])
        if float(tokens[3]) != 1.0 and tokens[1] == "OBSERVES":
            prob_instrument_names.append(tokens[0])
            prob_parameter_names.append(tokens[2])
            prob_probs.append(float(tokens[3]))

for i in range(len(instrument_names)):
    with open("/home/ben/repos/UKGE/KG processed data/en2id.txt", "r") as entity_file:
        for line in entity_file.readlines():
            line.rstrip()
            tokens = line.split("\t")
            if str(instrument_names[i]) == tokens[0].rstrip():
                instrument_id = tokens[1].rstrip()
                instrument_ids.append(instrument_id)
                break

for i in range(len(prob_parameter_names)):
    with open("/home/ben/repos/UKGE/KG processed data/en2id.txt", "r") as entity_file:
        for line in entity_file.readlines():
            line.rstrip()
            tokens = line.split("\t")
            if str(prob_parameter_names[i]) == tokens[0].rstrip():
                prob_parameter_id = tokens[1].rstrip()
                prob_parameter_ids.append(prob_parameter_id)
                break

for i in range(len(prob_instrument_names)):
    with open("/home/ben/repos/UKGE/KG processed data/en2id.txt", "r") as entity_file:
        for line in entity_file.readlines():
            line.rstrip()
            tokens = line.split("\t")
            if str(prob_instrument_names[i]) == tokens[0].rstrip():
                prob_instrument_id = tokens[1].rstrip()
                prob_instrument_ids.append(prob_instrument_id)
                break

for i in range(len(parameter_names)):
    with open("/home/ben/repos/UKGE/KG processed data/en2id.txt", "r") as entity_file:
        for line in entity_file.readlines():
            line.rstrip()
            tokens = line.split("\t")
            if str(parameter_names[i]) == tokens[0].rstrip():
                parameter_id = tokens[1].rstrip()
                parameter_ids.append(parameter_id)
                break


new_query_filename = 'new_query.tsv'
kg_tuples = []
with open(new_query_filename, "w") as query_file:
    for i in range(len(parameter_ids)):
        kg_tuples.append((instrument_ids[i],parameter_ids[i]))
        parameter_id = parameter_ids[i]
        instrument_id = instrument_ids[i]
        relation_id = "5"
        query_file.write(instrument_id + "\t" + relation_id + "\t" + parameter_id + "\t" + "1.00000" + "\n")

validator.build_by_file(new_query_filename, model_dir, model_filename, data_filename)
scores = validator.get_val()
plt.rcParams.update({'font.size': 12})
plt.hist(scores,density=True)
plt.title("Instrument/parameter pairs in KG")
plt.xlabel("UKGE score")
plt.ylabel("Density")
plt.savefig("KG_pairs.png",dpi=300)
plt.show()

random_query_filename = 'random_queries.tsv'
with open(random_query_filename, "w") as query_file:
    for i in range(1000):
        parameter_id = random.choice(parameter_ids)
        instrument_id = random.choice(instrument_ids)
        relation_id = "5"
        if (instrument_id,parameter_id) not in kg_tuples:
            query_file.write(instrument_id + "\t" + relation_id + "\t" + parameter_id + "\t" + "0.00000" + "\n")

validator.build_by_file(random_query_filename, model_dir, model_filename, data_filename)
scores = validator.get_val()
plt.hist(scores,density=True)
plt.title("Random instrument/parameter pairs")
plt.xlabel("UKGE score")
plt.ylabel("Density")
plt.rcParams.update({'font.size': 12})
plt.savefig("random_pairs.png",dpi=300)
plt.show()

prob_query_filename = 'prob_queries.tsv'
with open(prob_query_filename, "w") as query_file:
    for i in range(len(prob_parameter_ids)):
        prob_parameter_id = prob_parameter_ids[i]
        prob_instrument_id = prob_instrument_ids[i]
        relation_id = "5"
        query_file.write(prob_instrument_id + "\t" + relation_id + "\t" + prob_parameter_id + "\t" + str(prob_probs[i]) + "\n")

validator.build_by_file(prob_query_filename, model_dir, model_filename, data_filename)
scores = validator.get_val()
plt.scatter(scores,prob_probs)

x = np.linspace(0,1,1000)

m, b = np.polyfit(scores, prob_probs, 1)

line = m*x+b
plt.plot(x, line, 'r', label='y={:.2f}x+{:.2f}'.format(m,b))

plt.title("Paper-mined instrument/parameter pairs")
plt.xlabel("UKGE score")
plt.xlim([0,1])
plt.ylim([0,1])
plt.ylabel("Mined confidence score")
plt.legend()
plt.rcParams.update({'font.size': 12})
plt.savefig("mined_pairs.png",dpi=300)
plt.show()

# validator = UKGE_rect_Tester()
# instrument_name = 'OLI'
# parameter_name = 'Color dissolved organic matter (CDOM)'
# relation_name = 'OBSERVES'
# instrument_id = None
# parameter_id = None
# relation_id = None
# with open("../KG processed data/en2id.txt", "r") as entity_file:
#     for line in entity_file.readlines():
#         line.rstrip()
#         tokens = line.split("\t")
#         if instrument_name == tokens[0]:
#             instrument_id = tokens[1].rstrip()
#         if parameter_name == tokens[0]:
#             parameter_id = tokens[1].rstrip()
# with open("../KG processed data/rel2id.txt", "r") as relation_file:
#     for line in relation_file:
#         line.rstrip()
#         tokens = line.split("\t")
#         if relation_name == tokens[0]:
#             relation_id = tokens[1].rstrip()
# if instrument_id is None or parameter_id is None or relation_id is None:
#     print(instrument_id)
#     print(parameter_id)
#     print(relation_id)
#     print("invalid query")
#     exit()
# print(instrument_id.rstrip())
# print(parameter_id)
# print(relation_id)
# new_query_filename = 'new_query.tsv'
# with open(new_query_filename, "w") as query_file:
#     query_file.write(instrument_id + "\t" + relation_id + "\t" + parameter_id + "\t" + "1.00000" + "\n")
#     query_file.write(instrument_id + "\t" + relation_id + "\t" + parameter_id + "\t" + "1.00000" + "\n")

# validator.build_by_file(new_query_filename, model_dir, model_filename, data_filename)
# scores = validator.get_val()
# print(scores[0])

