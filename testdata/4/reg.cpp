#include<stdio.h>
#include <fstream>
#include <string>
#include<set>
#include<iostream>
#include<algorithm>
#include<regex>
using namespace std;
#define pred first 
#define class second 
vector<char> res;
int main(int argc, char* argv[]) {
    ifstream f_in;
    ifstream f_out;
    ifstream f_user;
    ofstream out("spjmsg.txt");
	int ret=0; //AC=0, WA=1, 其他均为 System Error
    
	/*****spj代码区域*******/
    // 以下是一个a+b的例子
    string str1;
    string str2;
    int cntp=0;
    typedef pair<double,int> P;
    vector<P> bufp;
    vector<P> bufn; 
    double iou=0;
    regex pattern("-[0-9]+(.[0-9]+)?|[0-9]+(.[0-9]+)?");
    str2="0.0050.5";
    cout<<regex_match(str2, pattern);
    
    


    return ret;//返回结果，返回值为0时，答案正确，为1时，答案错误，返回值为其他时，会报System Error
}