use std::{
    env,
    io::{
        self,
        prelude::*,
    },
    fs::File
};
mod consts;




const VERSION: &'static str = "v0.1.0-BETA";




fn main() -> io::Result<()> {
    let mut print: bool = true;
    let mut color: bool = true;


    let mut file = File::open(".enderpearl")?;
    let mut contents = String::new();
    file.read_to_string(&mut contents)?;
    let (_, tkn, _) = consts::Token::tokenize(contents);
    let mut arg: String = match env::args().nth(1) {
        Some(data) => data,
        None => String::from("")
    }.to_lowercase();
    for args in env::args() {
        if args.contains("--quiet") {
            print = false;
        }
        if args.contains("--no-color") || args.contains("--nocolor") {
            color = false;
        }
    }

    if arg.starts_with("--") {
        arg = arg.replace("--","");
        if arg == "help" {
            consts::help(color);
            return Ok(());
        } else if arg == "version" {
            println!("Version: {}",VERSION);
            return Ok(());
        } else {
            consts::help(color);
            return Ok(());
        }
    } else {
        if arg == "build" || arg == "." {
            consts::runcmd(String::from("build"),&tkn,print);
            return Ok(());
        } else if arg == "pre" || arg == "post" {
            println!("Sorry, you may not use this special operation");
            return Ok(());
        } else if arg == "" || arg == "help" {
            consts::help(color);
            return Ok(());
        } else {
            consts::runcmd(arg,&tkn,print);
            return Ok(());
        }
    }
}