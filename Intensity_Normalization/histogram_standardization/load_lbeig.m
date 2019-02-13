function lb_eig = load_lbeig(filename)


fid = fopen(filename);
s = textscan(fid,'%s','Delimiter','\n');
s = s{1};
temp_string = s{22};
string = temp_string(2:end); %Remove the bracket
lb_eig = str2num(string);
