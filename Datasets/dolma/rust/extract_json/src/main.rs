use serde::Deserialize;
use serde_json::Deserializer;
use std::fs::File;
use std::io::{BufReader, BufWriter, Write};
use structopt::StructOpt;

#[derive(StructOpt)]
struct Cli {
    /// The path to the JSON file
    input_file: String,
    /// The directory to save the output file
    output_dir: String,
    /// The chunk size for writing
    #[structopt(default_value = "100")]
    chunk_size: usize,
}

#[derive(Deserialize)]
struct Entry {
    text: String,
}

fn read_large_json(file_path: &str) -> impl Iterator<Item = Entry> {
    let file = File::open(file_path).expect("Unable to open file");
    let reader = BufReader::new(file);
    Deserializer::from_reader(reader).into_iter::<Entry>().map(|r| r.expect("Unable to parse JSON"))
}

fn extract_json_text(input_file: &str, output_dir: &str, chunk_size: usize) {
    let output_path = format!("{}/{}.txt", output_dir, std::path::Path::new(input_file).file_stem().unwrap().to_str().unwrap());

    let mut texts = Vec::new();
    let mut entry_count = 0;
    let file = File::create(output_path).expect("Unable to create output file");
    let mut writer = BufWriter::new(file);

    for entry in read_large_json(input_file) {
        texts.push(entry.text);
        entry_count += 1;
        if entry_count >= chunk_size {
            writer
                .write_all(texts.join("\n").as_bytes())
                .expect("Unable to write data");
            writer.write_all(b"\n").expect("Unable to write newline");
            texts.clear();
            entry_count = 0;
        }
    }

    if !texts.is_empty() {
        writer
            .write_all(texts.join("\n").as_bytes())
            .expect("Unable to write data");
        writer.write_all(b"\n").expect("Unable to write newline");
    }
}

fn main() {
    let args = Cli::from_args();

    extract_json_text(&args.input_file, &args.output_dir, args.chunk_size);
}

