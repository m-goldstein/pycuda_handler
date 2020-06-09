#define BLOCK_SIZE 512
#define BLOCK_MASK (BLOCK_SIZE)*2
__global__ void avg_kernel(float* in_vec, float* out_vec, int len)
{
    __shared__ float shared_seg_sum[2 * BLOCK_SIZE];
    unsigned int p = 0;
    do {
	if (len > blockIdx.x * BLOCK_MASK + threadIdx.x + p * BLOCK_SIZE)
	    shared_seg_sum[threadIdx.x + p * BLOCK_SIZE] = in_vec[blockIdx.x * BLOCK_MASK + threadIdx.x + p * BLOCK_SIZE];
	else
	    shared_seg_sum[threadIdx.x + p * BLOCK_SIZE] = 0.0f;
	p++;
    } while (p <= 1);
    
    for (unsigned int m = BLOCK_SIZE; m >= 1; m /= 2) {
	if (m > threadIdx.x) {
	    shared_seg_sum[threadIdx.x] += shared_seg_sum[threadIdx.x + m];
	}
	__syncthreads();
    }
    (threadIdx.x == 0) ? out_vec[blockIdx.x] = shared_seg_sum[threadIdx.x] / (1.0*len) : 0.0f;
}
