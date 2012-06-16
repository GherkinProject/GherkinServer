#include <iostream>
#include <fstream>
#include <string>
#include <vector>
using namespace std;

unsigned int split(const std::string &txt, std::vector<std::string> &strs, char ch)
{
    unsigned int pos = txt.find( ch );
    unsigned int initialPos = 0;
    strs.clear();

    // Decompose statement
    while( pos != std::string::npos ) {
        strs.push_back( txt.substr( initialPos, pos - initialPos + 1 ) );
        initialPos = pos + 1;

        pos = txt.find( ch, initialPos );
    }

    // Add the last one
    strs.push_back( txt.substr( initialPos, std::min( pos, txt.size() ) - initialPos + 1 ) );

    return strs.size();
}

int main(int argc, char** argv) {
    char* fileLoc(argv[0]);
    char* featLoc(argv[1]);

    ifstream reader(featLoc);

    string line;
    vector<string> extBase;     
    vector<string> tmp;

    while(getline(reader, line)) { 
        split(tmp, line, ":");
        extBase.push_back(tmp[0]);
    }
   
    cout << "extensions loaded" << endl;
 
    ofstream constFile('constant.csv');
    constFile << fileLoc;
    
    for(int i = extBase.begin(); i < extBase.end(); i++) {
        ifstream fileTmp((fileLoc + "." + extBase[i] + ".csv").c_str());
        cout << extBase[i] << " csv file loaded" << endl;
        double c(0);
        string row;
        vector<double> r;
        while(getline(fileTmp, row)) {            
            if(row[0] != '%') {
                split(tmp, row, ',');
                c++;
                try
                    for(int j = 0; j < tmp.size(); j++)
                        r[j] += double(row[j]) 
                catch()
                    for(int j = 0; j < tmp.size(); j++)
                        r.push_back(double(row[j]));
            }
        }
        r = (1 / c)*r;
    
        for(int j = r.begin(); j < r.end(); j++)
            constFile << "$" << r[j];
    }
    constFile << endl;
    
    return 0;
}
