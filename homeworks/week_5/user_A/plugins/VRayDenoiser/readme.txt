There are 2 ways to setup the VRayDenoiser for Nuke plugin:

1. Paste the VRayDenoiser folder and its contents in the plugin folder of the nuke installation you want to use with the plugin.
 - Windows: C:\Program Files\Common Files\NUKE\x.x\plugins\
 - Linux: /usr/local/NUKE/x.x/plugins/
 - OSX: /Library/Application Support/NUKE/x.x/plugins/ 
 Where <x.x> is the major.minor version of the NUKE in question.

2. Add the VRayDenoiser folder to the NUKE_PATH environment variable before running NUKE.
 example:
 - Windows: set NUKE_PATH=<path to plugin>/VRayDenoiser;%NUKE_PATH%
 - Linux/OSX: export NUKE_PATH=<path to plugin>/VRayDenoiser:$NUKE_PATH
 
How to use:

1. Start Nuke.

2. Find VRayDenoiser in the V-Ray Tools menu.

3. Load an image containing the denoising render elements(channels) exported from a V-Ray renderer.
 e.g. Load a multi channel .exr file with a read node.
4. Connect the denoising information to the VRayDenoiser Node. You can modify the channels using Nuke's operators before that.
The denoiser will notify you if there are render elements that are not present or recognised correctly. You can manually assign channels to their roles in the Channels tab.
5. General denoiser setting are found in the main tab. See https://docs.chaosgroup.com/display/VRAY3MAX/V-Ray+Denoiser+%7C+VRayDenoiser+ for more information.

Features:
1.4
 - Fix crash with 'frame blend' option in non-GUI mode
1.3
 - Enhance GPU memory management while denoising
 - Fix crash when denoising VRayRenderer node
1.2
 - Reading Alpha channel correctly
 - Update auto-assigning channels
1.1
 - If there is no 'noise level' channel you can set threshold
 - Denoising images with overscan
 - Can denoise an animation using multiple frames with the 'frame blend' option
1.0
 - Auto assign channels from input image as the channels used for denoising
 - Support for denoising on CPU/GPU/All OpenCL devices
