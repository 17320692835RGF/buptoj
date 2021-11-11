#include<stdio.h>
#include <fstream>
#include <string>
#include<set>
#include<iostream>
#include<algorithm>
using namespace std;
int main(int argc, char* argv[]) {
    ifstream f_in;
    ifstream f_out;
    ifstream f_user;
    f_in.open(argv[1]);
    f_out.open(argv[2]);
    f_user.open(argv[3]);
	int ret=0; //AC=0, WA=1, 其他均为 System Error

	/*****spj代码区域*******/
    // 以下是一个a+b的例子
    set<string> right;
    set<string> user;
    set<string> res;
    string str;
    float a,b;
    while(f_user>>str){
        user.insert(str);
    }

     while(f_out>>str){
        right.insert(str);
    }
    
    set_intersection(right.begin(),right.end(),user.begin(),user.end(),inserter( res , res.begin() ) );
    a=(float)res.size()/user.size();
    b=(float)res.size()/right.size();
    

	if(a>=0.9&&b>=0.9)
        ret=0;
    else 
        ret = 1;
	/*****spj-end********/ 
	f_in.close();
    f_out.close();
    f_user.close();

    //如果你想输出更多的信息，可以在同目录下，输出一个叫做 **spjmsg.txt** 的文件，当返回1时，系统会读取spjmsg.txt中的内容，显示在判题信息中。
    //如果你想输出更多的信息，可以在同目录下，输出一个叫做 **spjmsg.txt** 的文件，当返回1时，系统会读取spjmsg.txt中的内容，显示在判题信息中。
    //如果你想输出更多的信息，可以在同目录下，输出一个叫做 **spjmsg.txt** 的文件，当返回1时，系统会读取spjmsg.txt中的内容，显示在判题信息中。
    //重要事情说三遍，这样的话可以给用户更多的错误信息！！
    ofstream out("spjmsg.txt");
    if (out.is_open()) 
    {
        out << "召回率:"<<b<<" "<<"准确率:"<<a<<endl;
        out.close();
    }

    return ret;//返回结果，返回值为0时，答案正确，为1时，答案错误，返回值为其他时，会报System Error
}