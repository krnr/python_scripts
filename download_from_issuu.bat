mkdir 67
cd 67
for /L %%x in (1,1,84) do (
        ..\wget http://image.issuu.com/131021104237-7b890b7f6eb3c7fe4f2d6a3b94df3a66/jpg/page_%%x.jpg
) 