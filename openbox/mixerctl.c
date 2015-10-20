#include <alsa/asoundlib.h>

static snd_mixer_t *s_mixer = NULL;
static snd_mixer_elem_t *s_master = NULL;
int alsa_get_mute(snd_mixer_elem_t *s_master);
void alsa_set_mute(snd_mixer_elem_t *s_master, int mute);
int alsa_get_volume(snd_mixer_elem_t *s_master);
void alsa_set_volume(snd_mixer_elem_t *s_master,int vol);
void alsa_init(const char * chan);
void alsa_destroy();

int alsa_get_mute(snd_mixer_elem_t *s_master)
{
    int unmute;
    snd_mixer_selem_get_playback_switch(s_master,0,&unmute);
    return !unmute;
}

void alsa_set_mute(snd_mixer_elem_t *s_master, int mute)
{
    int chn;
    for (chn=0;chn<=SND_MIXER_SCHN_LAST;chn++) {
        snd_mixer_selem_set_playback_switch(s_master, chn, !mute);
    }
}

int alsa_get_volume(snd_mixer_elem_t *s_master)
{
  long al,ar;
  snd_mixer_selem_get_playback_volume(s_master, SND_MIXER_SCHN_FRONT_LEFT, &al);
  snd_mixer_selem_get_playback_volume(s_master, SND_MIXER_SCHN_FRONT_RIGHT, &ar);
  return (al+ar)>>1;
}

void alsa_set_volume(snd_mixer_elem_t *s_master,int vol)
{
  snd_mixer_selem_set_playback_volume(s_master, SND_MIXER_SCHN_FRONT_LEFT, vol);
  snd_mixer_selem_set_playback_volume(s_master, SND_MIXER_SCHN_FRONT_RIGHT, vol);
}


static void sevents_value(snd_mixer_selem_id_t *sid)
{
    fprintf(stderr,"something happend!\n");
    int mute = alsa_get_mute(s_master);
}

void alsa_init(const char * chan)
{
    int err;

    err = snd_mixer_open(&s_mixer,0);
    if(err){
        fprintf(stderr,"Mixer open error!\n");
        exit(1);
    }
       
 
    err = snd_mixer_attach(s_mixer,"default");
    if(err){
        fprintf(stderr,"Mixer attach error!\n");
        exit(1);
    }
    err = snd_mixer_selem_register(s_mixer,NULL,NULL);
    if(err){
        fprintf(stderr,"Mixer register error!\n");
        exit(1);
    }
    err = snd_mixer_load(s_mixer);
    if(err){
        fprintf(stderr,"Mixer load error!\n");
        exit(1);
    }
    s_master = snd_mixer_first_elem(s_mixer);
    while(strcmp(chan,snd_mixer_selem_get_name(s_master)))
        s_master = snd_mixer_elem_next(s_master);

    snd_mixer_selem_set_playback_volume_range(s_master, 0, 100);
}


void alsa_destroy()
{
    snd_mixer_close(s_mixer);
}



int main(int argc, char **argv)
{
    if(argc<=2){
        printf("Usage:mixerctrl Master <option>\n");
        printf(" <option> is one of below:\n");
        printf(" up    : volume up.\n");
        printf(" down  : volume down.\n");
        printf(" toggle: toggle mute/unmute.\n");
        printf(" mute  : mute\n");
        printf(" unmute: unmute\n");
        exit(0);
    }
    char cmd[100];
    if(argv[1])
        alsa_init(argv[1]);
    else
        alsa_init("Master");
    int cur = alsa_get_volume(s_master);
    
    if(strcmp(argv[2],"up")==0){
        int t = cur+10;
        if(t > 100)
            t = 100;
        if(alsa_get_mute(s_master))
            sprintf(cmd,"killall aosd_cat;echo \"Volume is: %d\%\"|aosd_cat -n \"Sans 40\" -R red -f 50 -o 50 -u 500 -p 4 -x 0&", t); 
        else
            sprintf(cmd,"killall aosd_cat;echo \"Volume is: %d\%\"|aosd_cat -n \"Sans 40\" -R green -f 50 -o 50 -u 500 -p 4 -x 0&", t); 
        system(cmd);
        alsa_set_volume(s_master,t);
    }
    if(strcmp(argv[2],"down")==0)
    {
        int t = cur-10;
        if(t <0)
            t = 0;
        if(alsa_get_mute(s_master))
            sprintf(cmd,"killall aosd_cat;echo \"Volume is: %d\%\"|aosd_cat -n \"Sans 40\" -R red -f 50 -o 50 -u 500 -p 4 -x 0&", t); 
        else
            sprintf(cmd,"killall aosd_cat;echo \"Volume is: %d\%\"|aosd_cat -n \"Sans 40\" -R green -f 50 -o 50 -u 500 -p 4 -x 0&", t); 
        system(cmd);
        alsa_set_volume(s_master,t);
    }
    if(strcmp(argv[2],"toggle")==0)
    {
        if(alsa_get_mute(s_master))
            sprintf(cmd,"killall aosd_cat;echo \"UnMute\"|aosd_cat -n \"Sans 40\" -R green -f 50 -o 50 -u 500 -p 4 -x 0&"); 
        else
            sprintf(cmd,"killall aosd_cat;echo \"Mute\"|aosd_cat -n \"Sans 40\" -R red -f 50 -o 50 -u 500 -p 4 -x 0&"); 
        system(cmd);
        alsa_set_mute(s_master,!alsa_get_mute(s_master));
    }

    if(strcmp(argv[2],"mute")==0)
    {
        alsa_set_mute(s_master,1);
    }

    if(strcmp(argv[2],"unmute") == 0)
    {
        alsa_set_mute(s_master,0);
    }

    if(s_mixer == NULL || s_master == NULL)
        exit(1);
}
