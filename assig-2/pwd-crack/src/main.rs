use reqwest::blocking::Client;
use reqwest::Error;

fn main() -> Result<(), Error> {
    let client = Client::new();

    let user_name = "cybersecurity".to_string();
    let password: Option<String> = Some("cybersecurity".to_string());

    let response = client
        .post("https://rs11.glorifykickstarter.com/wp-login.php")
        .basic_auth(user_name, password)
        .send();

    if response = Result<res> {

    }

    println!("{:?}", response);
    println!("{:?}", response.)

    Ok(())
}
