import os
import pycuda.autoinit
import pycuda.driver as drv
import numpy
import math
from pycuda.compiler import SourceModule
from handler import DBClient
from handler import HOST, PORT, USER, PASSWORD, DB_NAME
from feeder import init_client, vectorize_by_exchange
###################
BLOCK_SIZE = 512
TILE_SIZE  = 32
CUDA_KERNELS_PATH   = os.getcwd() + '/kernels/'
###################
s = ""
with open(CUDA_KERNELS_PATH+'avg_kern.cu') as fd:
    s = "".join([line for line in fd.readlines()])
mod = SourceModule(s)
avg_kern = mod.get_function('avg_kernel')

client          = init_client()
results         = client.make_query("execution_time", True, 100000)
exchange_vector = vectorize_by_exchange(results)

key_vector = [key for key in exchange_vector.keys()]
for key in key_vector:
	data_in  = exchange_vector[key]
	data_in  = numpy.asarray(data_in).astype(numpy.float32)
	data_out = numpy.zeros_like(data_in)
	input_size     = numpy.int32(len(data_in))
	print("Results for exchange %s"%(key))
	print("Input Vector: ")
	print(data_in)
	output_size = input_size / (BLOCK_SIZE << 1)
	if (input_size % (BLOCK_SIZE << 1)) != 0:
		output_size += 1
	blockDim = (BLOCK_SIZE, 1, 1)
	gridDim  = (math.ceil(output_size / (1.0 * TILE_SIZE)) * TILE_SIZE, 1, 1) 
	avg_kern(drv.In(data_in), drv.Out(data_out), input_size, block=blockDim, grid=gridDim)
	print("Output Vector: ")
	print(data_out[0])
print("\n")
