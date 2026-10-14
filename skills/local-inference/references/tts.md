# Qwen TTS

Adeck's other inference backend. It is not the LM Studio proxy on port 1234, and it does not wake zrrh.

The binary is `llama-tts`, the Vulkan build from `nix-os/modules/llama-tts.nix` (`GGML_BACKEND_PATH` set to `libggml-vulkan.so`). It runs on adeck's GPU. Weights live under `~/.lmstudio/models` and are loaded by this binary, not by the port 1235 server.

Babette calls it as a one-shot. The model files, speaker reference, and sampling flags are in `/mnt/echo/family-cookbook/babette/server.py`. Voice design stays there.
