#include <curl/curl.h>
#include <boost/asio.hpp>
#include <boost/beast/core.hpp>
#include <boost/beast/http.hpp>
#include <boost/serialization/string.hpp>
#include <boost/thread.hpp>
#include <iostream>
#include <nlohmann/json.hpp>
#include <boost/archive/text_oarchive.hpp>
#include <boost/archive/text_iarchive.hpp>

using namespace std;
using namespace nlohmann;
namespace asio = boost::asio;
namespace beast = boost::beast;
namespace http = beast::http;

class CurlHandler {
 public:
  CurlHandler() {}
  string fetch(const string& url) {
    CURL* curl = curl_easy_init();
    if (!curl) return "CURL initialization failed";

    string response;
    curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, writeCallback);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, &response);
    curl_easy_perform(curl);
    curl_easy_cleanup(curl);

    return response;
  }

 private:
  static size_t writeCallback(void* contents, size_t size, size_t nmemb,
                              void* userp) {
    ((string*)userp)->append((char*)contents, size * nmemb);
    return size * nmemb;
  }
};

class JsonParser {
 public:
  JsonParser() {}
  void parse(const string& jsonString) {
    auto parsedJson = json::parse(jsonString);
    cout << "Parsed JSON: " << parsedJson.dump(4) << endl;
  }
};

class HttpServer {
 public:
  HttpServer()
      : acceptor(ioContext,
                 asio::ip::tcp::endpoint(asio::ip::tcp::v4(), 8080)) {}
  void run() {
    startAccept();
    ioContext.run();
  }

 private:
  asio::io_context ioContext;
  asio::ip::tcp::acceptor acceptor;
  void startAccept() {
    auto socket = make_shared<asio::ip::tcp::socket>(ioContext);
    acceptor.async_accept(
        *socket, [this, socket](boost::system::error_code ec) {
          if (!ec) {
            string message =
                "HTTP/1.1 200 OK\r\nContent-Length: 13\r\n\r\nHello, World!";
            asio::async_write(*socket, asio::buffer(message),
                              [](boost::system::error_code, size_t) {});
          }
          startAccept();
        });
  }
};

class BoostThreadExample {
 public:
  void run() {
    boost::thread thread1(&BoostThreadExample::task1, this);
    boost::thread thread2(&BoostThreadExample::task2, this);
    thread1.join();
    thread2.join();
  }

 private:
  void task1() {
    for (int i = 0; i < 5; ++i) {
      cout << "Task 1 running: iteration " << i << endl;
    }
  }
  void task2() {
    for (int i = 0; i < 5; ++i) {
      cout << "Task 2 running: iteration " << i << endl;
    }
  }
};

class SerializationExample {
 public:
  SerializationExample() : data("Test data for serialization") {}
  string serialize() {
    stringstream ss;
    boost::archive::text_oarchive oa(ss);
    oa << data;
    return ss.str();
  }
  void deserialize(const string& serializedData) {
    stringstream ss(serializedData);
    boost::archive::text_iarchive ia(ss);
    ia >> data;
    cout << "Deserialized data: " << data << endl;
  }

 private:
  string data;
};

int main() {
  CurlHandler curlHandler;
  string urlResponse = curlHandler.fetch("http://www.example.com");
  cout << "Curl response: " << urlResponse << endl;
  string urlResponse2 = curlHandler.fetch("https://api.github.com/repos/nlohmann/json");

  JsonParser jsonParser;
  jsonParser.parse("{\"key\": \"value\"}");

  jsonParser.parse(urlResponse2);

  BoostThreadExample threadExample;
  threadExample.run();

  SerializationExample serializationExample;
  string serializedData = serializationExample.serialize();
  cout << "Serialized data: " << serializedData << endl;
  serializationExample.deserialize(serializedData);

  HttpServer server;
  boost::thread serverThread([&server]() { server.run(); });
  serverThread.join();

  return 0;
}
