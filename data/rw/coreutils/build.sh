git clone https://github.com/coreutils/coreutils.git
cd coreutils
git reset --hard 84f820228708fbee53e2267e6d2ad805197df8be
make -f cfg.mk
cd ..