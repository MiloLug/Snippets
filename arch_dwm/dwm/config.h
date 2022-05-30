/* See LICENSE file for copyright and license details. */

//keys
#include "XF86keysym.h"

/* appearance */
static const unsigned int borderpx  = 0;        /* border pixel of windows */
static const unsigned int snap      = 32;       /* snap pixel */
static const int showbar            = 1;        /* 0 means no bar */
static const int topbar             = 1;        /* 0 means bottom bar */
static const char *fonts[]          = { "monospace:size=8" };
static const char dmenufont[]       = "monospace:size=8";
static const char col_gray1[]       = "#111111";
static const char col_gray2[]       = "#444444";
static const char col_gray3[]       = "#bbbbbb";
static const char col_gray4[]       = "#eeeeee";
static const char col_cyan[]        = "#005577";
static const char *colors[][3]      = {
	/*               fg         bg         border   */
	[SchemeNorm] = { col_gray3, col_gray1, col_gray2 },
	[SchemeSel]  = { col_gray4, col_gray1,  col_cyan  },
};

/* tagging */
static const char *tags[] = { "1", "2", "3", "4", "5", "6", "7", "8", "9" };

static const Rule rules[] = {
	/* xprop(1):
	 *	WM_CLASS(STRING) = instance, class
	 *	WM_NAME(STRING) = title
	 */
	/* class      instance    title       tags mask     isfloating   monitor */
	{ "Gimp",     NULL,       NULL,       0,            1,           -1 },
	{ "Firefox",  NULL,       NULL,       1 << 8,       0,           -1 },
};

/* layout(s) */
static const float mfact     = 0.55; /* factor of master area size [0.05..0.95] */
static const int nmaster     = 1;    /* number of clients in master area */
static const int resizehints = 1;    /* 1 means respect size hints in tiled resizals */

static const Layout layouts[] = {
	/* symbol     arrange function */
	{ "[T]",      tile },    /* first entry is default */
	{ "[F]",      NULL },    /* no layout function means floating behavior */
	{ "[M]",      monocle },
};

/* key definitions */
#define MODKEY Mod1Mask
#define TAGKEYS(KEY,TAG) \
	{ MODKEY,                       KEY,      view,           {.ui = 1 << TAG} }, \
	{ ControlMask|ShiftMask,        KEY,      toggleview,     {.ui = 1 << TAG} }, \
	{ MODKEY|ControlMask,           KEY,      tag,            {.ui = 1 << TAG} }, \
	{ MODKEY|ControlMask|ShiftMask, KEY,      toggletag,      {.ui = 1 << TAG} },

/* helper for spawning shell commands in the pre dwm-5.0 fashion */
#define SHCMD(cmd) { .v = (const char*[]){ "/bin/sh", "-c", cmd, NULL } }

/* commands */
static char dmenumon[2] = "0"; /* component of dmenucmd, manipulated in spawn() */
static const char *dmenucmd[] = { "dmenu_run", "-m", dmenumon, "-fn", dmenufont, "-nb", col_gray1, "-nf", col_gray3, "-sb", col_cyan, "-sf", col_gray4, NULL };
static const char *termcmd[]  = { "kitty", NULL };

// volume
static const char *upvol1[]   = { "/usr/bin/pactl", "set-sink-volume", "1", "+5%",     NULL };
static const char *downvol1[] = { "/usr/bin/pactl", "set-sink-volume", "1", "-5%",     NULL };
static const char *mutevol1[] = { "/usr/bin/pactl", "set-sink-mute",   "1", "toggle",  NULL };
static const char *upvol2[]   = { "/usr/bin/pactl", "set-sink-volume", "0", "+5%",     NULL };
static const char *downvol2[] = { "/usr/bin/pactl", "set-sink-volume", "0", "-5%",     NULL };
static const char *mutevol2[] = { "/usr/bin/pactl", "set-sink-mute",   "0", "toggle",  NULL };

// brightness
static const char *upbrigh[] = { "/usr/bin/brightnessconf", "+5"};
static const char *downbrigh[] = { "/usr/bin/brightnessconf", "-5"};

//screenshot
static const char *fullscreenshot[] = { "screenshot",  NULL };
static const char *activescreenshot[] = { "screenshot", "window", NULL };
static const char *selectscreenshot[] = { "screenshot", "select", NULL };


/* KEYS */
static Key keys[] = {
	/* modifier                     key        function        argument */
	//Audio volume controls
	{ 0,              XF86XK_AudioLowerVolume, spawn,          {.v = downvol1 } },
	{ 0,              XF86XK_AudioMute,        spawn,          {.v = mutevol1 } },
	{ 0,              XF86XK_AudioRaiseVolume, spawn,          {.v = upvol1 } },
	
	{ ShiftMask,      XF86XK_AudioLowerVolume, spawn,          {.v = downvol2 } },
	{ ShiftMask,      XF86XK_AudioMute,        spawn,          {.v = mutevol2 } },
	{ ShiftMask,      XF86XK_AudioRaiseVolume, spawn,          {.v = upvol2 } },

	//Brightness controls
	{ 0,              XF86XK_MonBrightnessUp,  spawn,          {.v = upbrigh } },
	{ 0,             XF86XK_MonBrightnessDown, spawn,          {.v = downbrigh } },
	//Screenshots
	{ 0,                            XK_Print,  spawn,          {.v = fullscreenshot } },
	{ ControlMask,                  XK_Print,  spawn,          {.v = activescreenshot } },
	{ ShiftMask,                    XK_Print,  spawn,          {.v = selectscreenshot } },	

	//Other
	{ MODKEY,                       XK_r,      spawn,          {.v = dmenucmd } },
	{ MODKEY,                       XK_grave,  spawn,          {.v = termcmd } },
	{ MODKEY,                       XK_b,      togglebar,      {0} },

	{ MODKEY,                       XK_j,      focusstack,     {.i = +1 } },
	{ MODKEY,                       XK_k,      focusstack,     {.i = -1 } },
	
	{ MODKEY,                       XK_i,      incnmaster,     {.i = +1 } }, //change tiles variation
	{ MODKEY,                       XK_d,      incnmaster,     {.i = -1 } },

	{ MODKEY,                       XK_h,      setmfact,       {.f = -0.05} },
	{ MODKEY,                       XK_l,      setmfact,       {.f = +0.05} },
	{ MODKEY,                       XK_Return, zoom,           {0} }, //Switch between last tiles
	{ MODKEY,                       XK_Tab,    view,           {0} },
	{ MODKEY|ControlMask,           XK_c,      killclient,     {0} },
	{ MODKEY,                       XK_t,      setlayout,      {.v = &layouts[0]} },
	{ MODKEY,                       XK_f,      setlayout,      {.v = &layouts[1]} },
	{ MODKEY,                       XK_m,      setlayout,      {.v = &layouts[2]} },
//	{ MODKEY,                       XK_space,  setlayout,      {0} },
//	{ MODKEY|ControlMask,           XK_space,  togglefloating, {0} },
//	{ MODKEY,                       XK_0,      view,           {.ui = ~0 } },
//	{ MODKEY|ControlMask,           XK_0,      tag,            {.ui = ~0 } },
	
	//Monitors switching
	{ MODKEY,                       XK_comma,  focusmon,       {.i = -1 } },
	{ MODKEY,                       XK_period, focusmon,       {.i = +1 } },
	{ MODKEY|ControlMask,           XK_comma,  tagmon,         {.i = -1 } },
	{ MODKEY|ControlMask,           XK_period, tagmon,         {.i = +1 } },
	
	//Tags switching
	TAGKEYS(                        XK_1,                      0)
	TAGKEYS(                        XK_2,                      1)
	TAGKEYS(                        XK_3,                      2)
	TAGKEYS(                        XK_4,                      3)
	TAGKEYS(                        XK_5,                      4)
	TAGKEYS(                        XK_6,                      5)
	TAGKEYS(                        XK_7,                      6)
	TAGKEYS(                        XK_8,                      7)
	TAGKEYS(                        XK_9,                      8)
	{ ControlMask|ShiftMask,        XK_q,      quit,           {0} },
};

/* button definitions */
/* click can be ClkTagBar, ClkLtSymbol, ClkStatusText, ClkWinTitle, ClkClientWin, or ClkRootWin */
static Button buttons[] = {
	/* click                event mask      button          function        argument */
	{ ClkLtSymbol,          0,              Button1,        setlayout,      {0} },
	{ ClkLtSymbol,          0,              Button3,        setlayout,      {.v = &layouts[2]} },
	{ ClkWinTitle,          0,              Button2,        zoom,           {0} },
	{ ClkStatusText,        0,              Button2,        spawn,          {.v = termcmd } },
	{ ClkClientWin,  ControlMask|MODKEY,    Button1,        movemouse,      {0} },
	{ ClkClientWin,  ControlMask|MODKEY,    Button2,        togglefloating, {0} },
	{ ClkClientWin,  ControlMask|MODKEY,    Button3,        resizemouse,    {0} },
	{ ClkTagBar,            0,              Button1,        view,           {0} },
	{ ClkTagBar,            0,              Button3,        toggleview,     {0} },
	{ ClkTagBar,            MODKEY,         Button1,        tag,            {0} },
	{ ClkTagBar,            MODKEY,         Button3,        toggletag,      {0} },
};
