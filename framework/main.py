import container
import frida_manager
import repo_manager
import emulator_manager
import magisk_manager
import adeb_container
import adeb_manager
import kernel_repo_manager

if __name__ == '__main__':

   """
   AOSP section
   """
   arch = "x86_64"
   repoManager  = repo_manager.RepoManager(branch='android-10.0.0_r41')
   repoManager  = repo_manager.RepoManager(branch='android-11.0.0_r17')
   repoManager.repo_init()
   repoManager.repo_sync()
   container.create_ubuntu_container()
   container.run_ubuntu_container()

   """
   Android Kernel section
   """
   kernelRepoManager = kernel_repo_manager.KernelRepoManager(branch='q-goldfish-android-goldfish-4.14-dev')
   kernelRepoManager.repo_init()
   kernelRepoManager.repo_sync()
   kernelRepoManager.add_helloworld_ksource()
   kernelRepoManager.set_Kconfig()
   kernelRepoManager.set_Makefile()
   # kernelRepoManager.set_defconfig()
   kernelRepoManager.compile_kernel()
   

   """
   Emulator section
   """
   emuManager = emulator_manager.EmuManager()
   emuManager.start_emu()
   kernelRepoManager.push_module2emu()

   """
   Magisk section
   """
   magiskManager = magisk_manager.MagiskManager()
   magiskManager.clone_repo()
   magiskManager.set_config()
   magiskManager.build_ndk()
   magiskManager.build_all()
   magiskManager.install_magisk()
   magiskManager.start_magisk_deamon()

   """
   Frida Server section
   """
   fridaManager = frida_manager.FridaManager(architecture=arch)
   fridaManager.download_frida_server()
   fridaManager.extract_archive()
   frida_server_name = fridaManager.get_server_name()
   fridaManager.install_server()

   """adeb section"""
   adeb_container.create_ubuntu_container()
   adebManager = adeb_manager.AdebManager()
   adebManager.create_ubuntu_container()
   adebManager.run_ubuntu_container()
   adebManager.postinstall_setup()

