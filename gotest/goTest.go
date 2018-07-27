package main

import (
	"encoding/json"
	"fmt"
	"net/http"
)

func main() {
	fmt.Println("Hello, my dudes")
	resp, err := http.Get("http://api.bart.gov/api/etd.aspx?cmd=etd&orig=rock&key=ZSBD-57UA-9TVT-DWE9&dir=n&json=y")
	fmt.Println(err)
	defer resp.Body.Close()
	body, err := 
}

func getDepTimes() (ts []int, ok bool) {

}
