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
    f_in.open(argv[1]);
    f_out.open(argv[2]);
    f_user.open(argv[3]);
    ofstream out("spjmsg.txt");
	int ret=0; //AC=0, WA=1, 其他均为 System Error
    
	/*****spj代码区域*******/
    // 以下是一个a+b的例子
    string str1;
    string str2;
    string strbuf;
    int cntp=0;
    typedef pair<double,int> P;
    vector<P> bufp;
    vector<P> bufn; 
    double iou=0;
    regex pattern("-[0-9]+(.[0-9]+)?|[0-9]+(.[0-9]+)?");
    vector<string> fout;
    vector<string> fuser;
    while (getline(f_user,strbuf))
    {
        if(!regex_match(strbuf, pattern)){
            out<<"    格式错误    "<<strbuf;
            return 1;
        }
       fuser.push_back(strbuf);
    }
    while(getline(f_out,strbuf)){
        fout.push_back(strbuf);
    }
    if(fuser.size()-1<fout.size()){
        out<<"    格式错误,输出行数不对";
        return 1;
    }
    for(int i=0;i<fout.size();i++){
        str1=fout[i];
        str2=fuser[i];
        if(str1=="1"){
            bufp.push_back(make_pair(stod(str2),stoi(str1)));
        }
        else{
            bufn.push_back(make_pair(stod(str2),stoi(str1)));
        }
    }
    for(int i=0;i<bufp.size();i++){
        for(int j=0;j<bufn.size();j++){
            if(bufp[i].pred>bufn[j].pred){
                iou+=1;
            }
            else if(bufp[i].pred==bufn[j].pred){
                iou+=0.5;
            }
        }
    }
    iou=iou/(bufp.size()*bufn.size());
    out<<"****OJ计算的AUC ："<<iou<<"****用户输出的AUC："<<fuser[fuser.size()-1]<<"****";
	/*****spj-end********/ 
	f_in.close();
    f_out.close();
    f_user.close();

    return ret;//返回结果，返回值为0时，答案正确，为1时，答案错误，返回值为其他时，会报System Error
}