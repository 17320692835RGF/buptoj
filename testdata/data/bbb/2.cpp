#include<iostream>
using namespace std;
#define LOCAL
int res[27];
double cnt=0;
int main(){
    #ifdef LOCAL
        freopen("3.in", "r", stdin);
        freopen("3.out", "w", stdout);
    #endif // LOCAL
    // int a,b;
    // cin>>a>>b;
    // cout<<a<<" "<<b;
    string str;
    while(cin>>str){
        cnt+=10;
        for(auto it:str){
            res[it-'a']++;
        }
    }
    for(int i=0;i<26;i++){
        if(res[i]/cnt>=0.1){
            printf("%c %f\n",i+'a',res[i]/cnt);
        }
    }
    return 0;
}