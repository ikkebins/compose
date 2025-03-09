on Fedora-Coreos

podman run --name freeipa-server-container -ti -h my.hostname.zz --read-only -v ipa-data:/data:Z freeipa/freeipa-server:rocky-9