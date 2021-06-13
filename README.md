# Wacom Linux Movable Drawing Area

This is an attempt to solve the problem of using small graphics tablets for notetaking applications. 

When started, this creates a transparent gray rectangle of configurable size which corresponds to the area on the screen that your tablet is mapped to. By simply holding down spacebar you switch from the usual editing mode to movement mode. 

Now any movements of your pen will be translated to changes in the mapped area, such that the position of your cursor remains the same once you let go of the spacebar. 

Perhaps this is best illustrated by a video:

https://user-images.githubusercontent.com/26010054/121791788-1df23680-cbee-11eb-99b0-9a3a742fab9d.mp4

## Running

Really it could not be simpler. Simply execute the script with python(or add execute permissions) and pass in the fraction of the vertical height of your screen that you want your writing area to take up. As the first parameter. So for instance:
```
python WacomCustomMode.py 0.5
```
Will result in a rectangle with half the height of your screen and the aspect ratio of your tablet being made available for writing.

## Some notes

### Compositors

For me it was necessary to disable blur in my compositor. For [picom](https://github.com/yshui/picom)/formerly compton this can be done with something like the following:
```
blur-background-exclude = [
    "class_g = 'WacomCustomMode.py'"
];
```
Note that I am using the class name here which is somewhat hard to configure in QT. It defaults to the name of the script, so this might require some changes should you say put this into your `bin` folder.

For other compositors I am not quite sure how it could be done, but I believe KWin offers similar options for individual applications.

### Tested Tablets

I myself have only tried this with a One by Wacom Small. If this works for you on some other tablet, do let me know.

### But I need my spacebar!

Well, I too faced this problem too. I personally don't believe you always need to have the script running and even when running it doesn't really interfer with anything so long as you don't intend to type and write by hand at the same time.

What may be an issue though is if your notetaking application itself has the spacebar mapped. This is the case for [Xournal++](https://xournalpp.github.io/), where the spacebar scrolls down. This is not configurable, but it really is quite easy to remove that functionality with the patch in this repository and the compile it yourself. Instructions for compilation can be found [here](https://github.com/xournalpp/xournalpp/blob/master/readme/LinuxBuild.md). 

## Backstory

I originally got a graphic tablet primarily for attempting to digitize some of my less structured notes(i.e. not practical to do in LaTeX even with the help of [some rather powerful shortcuts](https://castel.dev/)) as well as for doing the homework for a course that didn't permit doing it in LaTex(crazy, right?). 

Since I didn't intend to use it a whole lot and COVID is (hopefully) soon-to-be-over in Europe, I didn't really want to spend all too much money. I therefore got the cheapest Wacom Tablet there is, as I was unsure of the driver situation on Linux, but that obviously meant I only got a 152x95mm Tablet. But no matter I thought, this is basically A5, that's plenty. 

Turns out, I was wrong. Not only did having such a small area map to an entire 27' screen feel totally jarring, I couldn't even write small enough to fit an entire line on the thing without having my hand going off the other side. Thinking this must be a common problem, I was certain that realtive mode must be something exactly like what this tool now exists to provide, but I soon realized it wasn't.

Therefore I set out to make this tool. While I had no real experience with xinput or QT I managed to get it up and running in a couple of days of work. Meaning I could now always write in areas of the tablet that were fairly comfortable.

It indeed turned out to help quite a bit, and a friend that uses a Surface(I consider them overpriced for the specs) also confirmed that she also liked to scroll the page while writing. 

However while this was an improvement, on the whole it still couldn't beat paper. While it gave me the ability to make changes after the fact much more easily, the fact I was still in the return window of the tablet and that it still wasn't completely natural even with some practice, made me come to the conclusion that it would be best to simply send it back. 

But given that I'd invested a good 10 hours or so into making this and I decided to simply put it on GitHub and see if anyone was interested in trying for themselves. Maybe with some further improvements(like making the buttons on the pen work properly, I couldn't make that work because you always get `ButtonRelease` events when moving out of proximity with the pen which was jittery) this could actually become more usable.

It might also be that there is a sweetspot of tablet size where this just about makes it viable. That too I have not explored.

## Contributions and Ideas

Should anyone actually turn out to be interested in this project and using it, any contributions or ideas would of course be appreciated. 

I don't know if anyone might want Windows support for this, and I have honestly no idea how one might implement that, but that is certainly something this is missing.
