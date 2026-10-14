# GPU

Portable extract from nixarchy `nixos-gpu` (MIT, Copyright (c) 2026 Olaf Krasicki Freund and the nixarchy contributors, upstream commit `d1afbdda4126402275ac5de42470f4b623fb4069`). The full skill, including NixOS driver snippets, Hyprland, PRIME, and containers, stays at `skills/upstream/nixarchy/nixos-gpu/SKILL.md`.

This mesh serves chat from LM Studio's bundled llama.cpp on zrrh. That binary is not `pkgs.llama-cpp`. `nixpkgs.config.cudaSupport` does not retarget it.

## Three layers

A model on CPU, or a GPU "not detected", is one of these. Walk them in order.

| Layer | What it is | Check |
|---|---|---|
| 1. Kernel driver | The GPU shows up at all | `lspci -nn`, `lsmod` for `nvidia` or `amdgpu` |
| 2. Userspace | The runtime can see the card | `nvidia-smi`, or `rocminfo` / `vulkaninfo --summary` |
| 3. Application build | This binary was compiled with that GPU | A CUDA-less PyTorch or llama.cpp on a working driver still runs on CPU |

Identify the card before changing a driver branch. A kernel-module change needs a reboot. `nixos-rebuild switch` alone leaves the old module loaded.

## This mesh

| Host | GPU | Inference role |
|---|---|---|
| zrrh | NVIDIA RTX 4090, 24 GB | Chat. LM Studio llama.cpp, CUDA. |
| nxiz | NVIDIA RTX 3070 | Workstation. The 4B embedding model can load here. |
| adeck | AMD Vangogh, Vulkan | Wake proxy and LM Link. Not the large-model GPU. |

## A Nix-built CUDA binary

`libcuda.so.1` is at `/run/opengl-driver/lib`. A "cannot find libcuda.so.1" error on a Nix-built binary is that path missing from `LD_LIBRARY_PATH`.

Prefer one package over the global flag:

```nix
(pkgs.llama-cpp.override { cudaSupport = true; })
```

`nixpkgs.config.cudaSupport = true` (and `rocmSupport`) changes build inputs across a large part of nixpkgs. Expect a long rebuild. `nixpkgs.config.cudaCapabilities` limits that compile to listed SMs. The nixarchy example for an RTX 4090 is `"8.9"`. Read the card before writing the list.

`hardware.nvidia.open = true` is the open kernel modules, for Turing and newer. `false` is for Maxwell, Pascal, and Volta. The option has no default.

## AMD compute

`amdgpu` is in the kernel. Graphics can work with no extra driver. ROCm is the compute stack. The user needs the `video` and `render` groups, or `rocminfo` shows nothing.

A card outside AMD's support list often works after `HSA_OVERRIDE_GFX_VERSION` is set to the nearest supported architecture, rounded down. Read `rocminfo | grep -i gfx`. `gfx1030` is `"10.3.0"`. `HSA_STATUS_ERROR_INVALID_ISA` or `hipErrorNoBinaryForGpu` is this miss. adeck is not where the large models run. Do not invent an override for Vangogh from this note.

## Left in the upstream skill

Black screen after a driver change, PRIME bus IDs, container GPU passthrough, Intel VA-API, and the reboot-versus-`switch` recovery path. Those are host setup. They are not a model preset.
