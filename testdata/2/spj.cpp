#include<stdio.h>
#include <fstream>
#include <string>
#include<set>
#include<iostream>
#include<algorithm>
#include<regex>
using namespace std;
double res1[27];
double res2[27];
double res3[27];
int cnt2=0;
int cnt1=0;
int cnt3=0;
vector<char> res;
int main(int argc, char* argv[]) {
    ifstream f_in;
    ifstream f_out;
    ifstream f_user;
    f_in.open(argv[1]);
    f_out.open(argv[2]);
    f_user.open(argv[3]);
    ofstream out("spjmsg.txt");
	int ret=0; //AC=0, WA=1, 其他均为 System Error
    
	/*****spj代码区域*******/
    // 以下是一个a+b的例子
    string str;
    regex pattern("[a-z] -?(([1-9]\\d*\\.\\d*)|(0\\.\\d*[1-9]\\d*))");
    while(getline(f_in,str)){
        cnt3+=10;
        for(auto it:str){
            res3[it-'a']++;
        }
    }
    for(int i=0;i<26;i++){
        res3[i]=res3[i]/cnt3;
    }
    while(getline(f_out,str)){
        char a;
        double b;
        sscanf(str.c_str(),"%c %lf",&a,&b);
        cnt1+=1;
        res1[a-'a']=b;
    }
    while(getline(f_user,str)){
        char a;
        double b;
        if(!regex_match(str, pattern)){
            out<<"   输出格式不对";
            return 1;
        }
        sscanf(str.c_str(),"%c %lf",&a,&b);
        if(res2[a-'a']!=0){
            out<<"   输出格式不对";
            return 1;
        }
        if(res3[a-'a']<0.09){
            out<<"   "<<(char)(a)<<"不是频繁项"<<endl;
            return 1;
        }
        res2[a-'a']=b;
        if(res1[a-'a']!=0){
            cnt2+=1;
        }
        else{
            out<<"   "<<(char)(a)<<"是误报项,其实际支持度为"<<res3[a-'a']<<endl;
        }
    }
    if(cnt1==cnt2){
        for(int i=0;i<26;i++){
            if(abs(res2[i]-res3[i])>0.01&&res2[i]!=0){
                ret=1;
                out<<"   "<<(char)(i+'a')<<"误差大于0.01"<<endl;
            }
        }
    }
    else{
        out<<"   频繁项没找全";
        return 1;
    }

	/*****spj-end********/ 
	f_in.close();
    f_out.close();
    f_user.close();

    //如果你想输出更多的信息，可以在同目录下，输出一个叫做 **spjmsg.txt** 的文件，当返回1时，系统会读取spjmsg.txt中的内容，显示在判题信息中。
    //如果你想输出更多的信息，可以在同目录下，输出一个叫做 **spjmsg.txt** 的文件，当返回1时，系统会读取spjmsg.txt中的内容，显示在判题信息中。
    //如果你想输出更多的信息，可以在同目录下，输出一个叫做 **spjmsg.txt** 的文件，当返回1时，系统会读取spjmsg.txt中的内容，显示在判题信息中。
    //重要事情说三遍，这样的话可以给用户更多的错误信息！！
    return ret;//返回结果，返回值为0时，答案正确，为1时，答案错误，返回值为其他时，会报System Error
}