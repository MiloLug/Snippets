#include <X11/Xlib.h>
#include <X11/Xutil.h>
#include <X11/Xos.h>

#include <stdio.h>
#include <stdlib.h>
// password checking
#include <pwd.h>
#include <shadow.h>
#include <sys/types.h>
#include <unistd.h>

#include <string>
using namespace std;

Display *dis;
int screen;
int depth;
Screen* selected_screen;
Window win;
GC gc;
XSetWindowAttributes attributes;
Visual *visual;

unsigned long _RGB(int r,int g, int b){
    return b + (g<<8) + (r<<16);
}
void init_x();
void close_x();
void redraw();

void print_xy(const char *str, int x, int y){
	XSetForeground(dis,gc,_RGB(255, 255, 255));
	XDrawString(dis,win,gc,x,y, str, strlen(str));
}

void collectstrings(const char * const *strs, char *result){
	for(;*strs != NULL; strs++){
		strcpy(result, *strs);
		result += strlen(*strs);
	}
}

bool check_password(const char *username, const char *password){
	struct spwd *shadow;
	char *p, *correct, *supplied, *salt;
	
	/* Read the correct salt from the shadow entry */
	shadow = getspnam(username);
	if (shadow == NULL) return 0;
	correct = shadow->sp_pwdp;
	if(correct == NULL || !strlen(correct)) return 0;
	
	/* Extract the salt */
	salt = strdup(correct);
	p = strchr(strchr(salt+1, '$')+1, '$');
	*(p++) = 0;
	//check and remove
	supplied = crypt(password, salt);
	bool r = !strcmp(supplied, correct);
	delete[] salt;
	return r;
}

int main (int argc, char **argv) {
	XEvent event;		/* the XEvent declaration !!! */
	KeySym key;		/* a dealie-bob to handle KeyPress Events */
	char raw_input[8];
	char tmp_input[64];
	char hidden_input[64];
	int input_len = 0;
	const int max_input_len = 63;
	tmp_input[0] = 0;

	char out_text[255];
	out_text[0] = 0;

	if(argc < 2) return 1;
	char *username = argv[1];
	static const char *results[] = {username, " > ", hidden_input, "_", NULL};

	init_x();
	/* look for events forever... */
	while(1) {
		/* get the next event and stuff it into our event variable.
		* Note:  only events we set the mask for are detected!
		*/
		XNextEvent(dis, &event);
		
		if (event.type == KeyPress && XLookupString(&event.xkey, raw_input, 8, &key, 0) == 1) {
			switch(key){
			case XK_Return:
				if(check_password(username, tmp_input))
					_exit(0);
				else
					tmp_input[0] = 0,
					input_len = 0;
				break;
			case XK_BackSpace:
				if(input_len)
					tmp_input[--input_len] = 0;
				break;
			default:
				if(input_len < max_input_len)
					tmp_input[input_len] = raw_input[0],
					tmp_input[++input_len] = 0;
			}

		}
		for(int l = 0; l < input_len; l++) hidden_input[l] = '*';
		hidden_input[input_len] = 0;
		collectstrings(results, out_text);
		
		redraw();
		print_xy(out_text, 20, 20);
	}

	return 0;
}

void init_x() {
/* get the colors black and white (see section for details) */
	int state;

	unsigned long black,white;

	dis = XOpenDisplay((char *)0);
   	screen = DefaultScreen(dis);
	visual = DefaultVisual(dis, screen);
	depth = DefaultDepth(dis, screen);
	selected_screen = ScreenOfDisplay(dis, screen);
	
	attributes.background_pixel = BlackPixel(dis, screen);
	attributes.override_redirect = true;
	attributes.do_not_propagate_mask = KeyPress|KeyRelease;
	attributes.bit_gravity = StaticGravity;

	win=XCreateWindow(dis, XRootWindow(dis, screen),
	0, 0, selected_screen->width, selected_screen->height, 0,
		depth, InputOutput,
		visual, CWBackPixel|CWOverrideRedirect|CWDontPropagate|CWBitGravity, &attributes);
	
	XMapWindow(dis, win);
	XRaiseWindow(dis, win);
	
	XSelectInput(dis, win, ExposureMask|KeyPressMask);
        gc=XCreateGC(dis, win, 0,0);
	XSetInputFocus(dis, win, RevertToParent, CurrentTime);
	XUngrabKeyboard(dis, 0);
	XGrabKeyboard(dis, DefaultRootWindow(dis), true, GrabModeAsync, GrabModeAsync, CurrentTime);
}

void close_x() {
	XFreeGC(dis, gc);
	XDestroyWindow(dis,win);
	XCloseDisplay(dis);
	exit(1);
}

void redraw() {
	XClearWindow(dis, win);
}
