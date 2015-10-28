package main

import (
	/* 引入各种需求的库*/
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
	/* 构建falcon可以接收的数据结构 */
	Endpoint    string  `json:"endpoint"`
	Metric      string  `json:"metric"`
	Timestamp   int     `json:"timestamp"`
	Step        int     `json:"step"`
	Value       float64 `json:"value"`
	CounterType string  `json:"counterType"`
	Tags        string  `json:"tags"`
}

/* 定义了一些初始化变量，*/
var filename string = os.Args[1] //定义用户输入的文件名
var quit chan int                //定义了channel
var chk int = 0                  //定义了循环的计数器
var strs []json_data
var cur_time int //当前时间戳
var url string   //url

func add_json(in json_data) []json_data {
	// 把json格式的文本导入json串中
	strs = append(strs, in)
	return strs
}

func decode_json(in_value float64, in_tag string, in_time int) json_data {
	// 解析成json格式的数据，本样例中因为是存活监控，因此是GAUGE类型，大部分项目为固定项目。
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
	// 错误检查
	if err != nil {
		fmt.Fprintf(os.Stderr, "Fatal error: %s", err.Error())
		os.Exit(1)
	}
}

func mon(ip string, in_time int) {
	// 根据用户输入的IP，建立TCP连接，超时时间为10秒，如正常返回1，异常为0
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
	//初始化时间戳
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
	//86 - 102 以行读入文件，并简历goruntime进行检查
	quit = make(chan int, chk)
	for i := 0; i < chk; i++ {
		<-quit
	}
	//检查chan是否结束
	b, _ := json.Marshal(strs)
	// os.Stdout.Write(b)
	url = "http://127.0.0.1:1988/v1/push"
	resp, err := http.Post(url, "application/json", strings.NewReader(string(b)))
	if err != nil {
		fmt.Print(err)
	}
	defer resp.Body.Close()
	// 108 - 116 push数据
}

