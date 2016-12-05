-- 分割字符串
create function f_split(@c text,@split varchar(32)) 
returns @t table(col varchar(20)) 
as 
begin 
while(charindex(@split,@c)<>0) 
begin 
insert @t(col) values (substring(@c,1,charindex(@split,@c)-1)) 
set @c = stuff(@c,1,charindex(@split,@c),'') 
end 
insert @t(col) values (@c) 
return 
end 
go 

create procedure p_add_thread_posts(fid int, usr char(15), subject char(80), posts_str text)
begin


end$