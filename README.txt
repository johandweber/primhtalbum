primhtalbum - A primitive HTML image album generator program
============================================================

primhtalbum (Primitive HTML album) is an interactive
python3 script that creates a very simple web gallery.
It does not intend to compete with any other of the many
other webgallery programs and should rather be considered as
a python exercise.
Still I consider it quite useful if the aim is to distribute
just a photo album based on an uncomplicated HTML interface.
The script requires the presence of the standard UNIX file
delete command "rm", the "zip" command line program as well as the
"convert" an the "mogrify" programs from the Image Magick
package. These programs can be easily installed from the
package systems of all maior linux distributions (the program
has been tested using Ubuntu 18.04) but are also available for
other UNIX-like environments like MacOS X, Cygwin, or MSYS2.

The to run the program, just enter the directory where the
images you want to use in your album are (subdirectories are
not considered). Then call, the script.
This can also either by done by calling
"python3 PATH_WHERE_YOUR_SCRTIPT_IS/primhtalbum.py"
or by putting the script in your executable search path,
making it executable (e.g. by "chmod +x primhtalbum") and
just calling "primhtalbum.py".
After that you will be interactively asked the title of the
album and the size of the prview and the gallery pictures
(the original images remain available).


(c) 2019-2024 by Johann Andreas Weber
