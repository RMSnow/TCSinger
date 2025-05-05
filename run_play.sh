export PYTHONPATH="/storage/zhangxueyao/workspace/TCSinger"

CUDA_VISIBLE_DEVICES=6 python inference/style_transfer.py \
    --config egs/sdlm.yaml \
    --exp_name checkpoints/SDLM