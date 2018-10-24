import Foundation
import PlaygroundSupport
PlaygroundPage.current.needsIndefiniteExecution = true

let path = "Resources/billboard.json"

// Since our data is static and never changes, we will be reading in from a local JSON file. This file will contain data scraped on music charts from billboard.com. See folder billboard_scraping for scraping code.

// The dataset attached to this playground contains a subset of the eventual dataset due to the long time it takes to scrape. This dataset contains data from January 1959 through February 1959. The eventual data set will contain data from 1959 to 2017.

struct Result: Decodable {
  let songs: [Song]
  
  enum CodingKeys : String, CodingKey {
    case songs
  }
}

struct Song: Decodable {
  let date: String
  let title: String
  let artist: String
  let url: String
  
  enum CodingKeys : String, CodingKey {
    case date
    case title
    case artist
    case url
  }
}
let fileURL = Bundle.main.url(forResource: "billboard", withExtension: "json")

let task = URLSession.shared.dataTask(with: fileURL!) { (data, response, error) in
  guard let data = data else {
    print("Error: No data to decode")
    return
  }

  guard let result = try? JSONDecoder().decode(Result.self, from: data) else {
    print("Error: Couldn't decode data into a result")
    return
  }

  print("Top Songs:")
  print("--------------")
  for song in result.songs {
    print("Top Song for: \(song.date)")
    print("- artist: \(song.title)")
    print("- title: \(song.artist)")
    print("- url: \(song.url)")
  }

}

task.resume()
