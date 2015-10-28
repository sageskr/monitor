package main

import (
	"bufio"
	"encoding/json"
	"fmt"
	"io"
	"net"
	"net/http"
	"os"
	"strings"
	"time"
)

type json_data struct {
	Endpoint    string  `json:"endpoint"`
	Metric      string  `json:"metric"`
	Timestamp   int     `json:"timestamp"`
	Step        int     `json:"step"`
	Value       float64 `json:"value"`
	CounterType string  `json:"counterType"`
	Tags        string  `json:"tags"`
}

var filename string = os.Args[1]
var quit chan int
var chk int = 0
var strs []json_data
var cur_time int
var url string

func add_json(in json_data) []json_data {
	strs = append(strs, in)
	return strs
}

func decode_json(in_value float64, in_tag string, in_time int) json_data {
	j_tags := "ip=" + in_tag
	s := json_data{
		Endpoint:    `test_localhost`,
		Metric:      `test_metric`,
		Timestamp:   in_time,
		Step:        60,
		Value:       in_value,
		CounterType: `GAUGE`,
		Tags:        j_tags,
	}
	return s
}

func checkError(err error) {
	if err != nil {
		fmt.Fprintf(os.Stderr, "Fatal error: %s", err.Error())
		os.Exit(1)
	}
}

func mon(ip string, in_time int) {
	var ip_port string = ip
	timeOut := time.Duration(10) * time.Second
	conn, err := net.DialTimeout("tcp", ip_port, timeOut)
	if err != nil {
		// fmt.Printf("%s is fail\n", ip)
		s := decode_json(0.0, ip, in_time)
		strs = add_json(s)
		quit <- 0
		return
	} else {
		// fmt.Printf("%s is ok\n", ip)
		s := decode_json(1.0, ip, in_time)
		strs = add_json(s)
		quit <- 0
		return
	}
	defer conn.Close()
}
func main() {
	cur_time := int(time.Now().Unix())
	fo, err := os.Open(filename)
	if err != nil {
		panic(err)
	}
	defer fo.Close()
	read_cursor := bufio.NewReader(fo)
	for {
		line, err := read_cursor.ReadString('\n')
		if err != nil || io.EOF == err {
			break
		}
		line = strings.TrimRight(line, "\n")
		s_line := string(line) + ":22"
		chk += 1
		go mon(s_line, cur_time)
	}
	quit = make(chan int, chk)
	for i := 0; i < chk; i++ {
		<-quit
	}
	b, _ := json.Marshal(strs)
	// os.Stdout.Write(b)
	url = "http://127.0.0.1:1988/v1/push"
	resp, err := http.Post(url, "application/json", strings.NewReader(string(b)))
	if err != nil {
		fmt.Print(err)
	}
	defer resp.Body.Close()
}

