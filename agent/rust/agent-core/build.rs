fn main() {
    println!("cargo:rerun-if-changed=../../ipc/proto/agent_ipc.proto");
    let proto_path = "../../ipc/proto/agent_ipc.proto";
    let out_dir = std::path::PathBuf::from(std::env::var("OUT_DIR").expect("OUT_DIR missing"));
    let _ = prost_build::Config::new()
        .out_dir(out_dir)
        .compile_protos(&[proto_path], &["../../ipc/proto"]);
}
