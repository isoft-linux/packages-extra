crate_uris(){
	while (( "$#" )); do
		local name version url
		name="${1%-*}"
		version="${1##*-}"
		url="https://crates.io/api/v1/crates/${name}/${version}/download"
		# -> ${1}.crate"
		echo $url
		wget $url -O ${1}.crate
		shift
	done
}

CRATES="bitflags-0.1.1
curl-0.2.10
curl-sys-0.1.24
docopt-0.6.67
env_logger-0.3.1
filetime-0.1.4
flate2-0.2.7
gcc-0.3.8
git2-0.2.11
git2-curl-0.2.4
glob-0.2.10
libc-0.1.8
libgit2-sys-0.2.17
libssh2-sys-0.1.25
libz-sys-0.1.6
log-0.3.1
matches-0.1.2
miniz-sys-0.1.5
num_cpus-0.2.6
openssl-sys-0.6.2
pkg-config-0.3.4
regex-0.1.30
rustc-serialize-0.3.14
semver-0.1.19
strsim-0.3.0
tar-0.2.14
term-0.2.9
threadpool-0.1.4
time-0.1.26
toml-0.1.21
url-0.2.35
"
crate_uris $CRATES
