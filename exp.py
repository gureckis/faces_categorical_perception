#!/usr/bin/pythonw
####
# Unsupervised Clustering in Supervised Categories
# one condition: training
# programmed: Oct. 11th, 2006
# data collected ?th, 2006
####

###########################################################
## to do list: 
##
##
###########################################################

###########################################################
# to build in pygame: 
#    - python setup.py py2app
#
###########################################################

###########################################################
##
##
###########################################################

###########################################################
# import modules 
###########################################################
import os, sys, signal
import math
#from Numeric import *
from ftplib import FTP
from random import random, randint, shuffle
from numpy.numarray import random_array, numerictypes
import pygame
from pygame.locals import *
import tempfile
from time import sleep

###########################################################
# defines 
###########################################################
laptop = True
laptopres = (1024, 768)
fullscreenres = (1440, 900)
#fullscreenres = (1024, 768)

NBLOCKS = 3
LEARNBLOCKTRIALS = 10 
PRETEST = True
TRAINING = True
POSTTEST = True
N_TEST_BLOCKS = 2

#### COLORS
white = (255, 255, 255)
grey = (175,175,175)
black = (0, 0, 0)
blue = (0, 0, 175)
green = (0,175,0)
ltgrey = (211,211,211)

#### CONDITIONS
HOR_AB = 0
HOR_BA = 1
VERT_AB = 2
VERT_BA = 3

CLUSTERING = 0
NOCLUSTER = 1
VERBALTASK = 2
SPATIALTASK = 3

HOR_RULE = 0
VERT_RULE = 1
AB = 0
BA = 1

A = 0
B = 1

WITHIN_CLUSTER_HORIZ = 1
WITHIN_CLUSTER_VERT = 2
WITHIN_CLUSTER_DIAG = 3
        
BETWEEN_CLUSTER_VERT = 4
BETWEEN_CLUSTER_DIAG = 5
        
BETWEEN_CATEGORY_HORIZ = 6
BETWEEN_CATEGORY_DIAG = 7

experimentname = 'cluster sensitivity'
trialtypes = {"instruction":0, "training":1, "break":2, "xab-test":3, "xab-pretest":4, "xab-traintest":5, "dualtaskstudy":6, "dualtasktest":7}
    
###########################################################
# Experiment Class
###########################################################
class Experiment:
    def __init__(self):

        # initalize pygame
        pygame.init()
        if laptop:
            self.screen = pygame.display.set_mode(laptopres, HWSURFACE|DOUBLEBUF)
        else:
            self.screen = pygame.display.set_mode(fullscreenres, HWSURFACE|DOUBLEBUF|FULLSCREEN) 
        pygame.display.set_caption(experimentname)
        pygame.mouse.set_visible(0)
        
        self.expstart = pygame.time.get_ticks()

        [self.cond, self.ncond, self.subj] = self.get_cond_and_subj_number('patterncode.txt')
        
        if 0 <= self.subj%16 <= 3:
            self.rule = 0
            self.order = 0
        elif 4 <= self.subj%16 <= 7:
            self.rule = 0
            self.order = 1
        elif 8 <= self.subj%16 <= 11:
            self.rule = 1
            self.order = 0
        elif 12 <= self.subj%16 <= 15:
            self.rule = 1
            self.order = 1

        self.load_all_resources('images')
        self.trial = 0      
        self.filename = "data/%s.dat" % self.subj
        self.datafile = open(self.filename, 'w')
        self.block = 0

    
        print "I am subject %s in condition %s" % (self.subj, self.cond)
        self.datafile.write("I am subject %s in condition %s\n" % (self.subj, self.cond))

        if self.rule == HOR_RULE:
            print "I am using a horizontal rule"
            self.datafile.write("I am using a horizontal rule\n")
        elif self.order == VERT_RULE: 
            print "I am using a vertical rule"
            self.datafile.write("I am using a vertical rule\n")
        if self.order == AB:
            print "I am using a AB rule"
            self.datafile.write("I am using a AB rule\n")
        elif self.order == BA:
            print "I am using a BA rule"
            self.datafile.write("I am using a BA rule\n")
        
        if PRETEST:
            print "I ran in the multi-test condition"
            self.datafile.write("I ran in the multi-test condition\n")
        else:
            print "I ran in the single test condition"
            self.datafile.write("I ran in the single test condition\n")
        



    ###########################################################
    # do_regular_exp
    ###########################################################
    def do_regular_exp(self):

        if PRETEST:
            ## break with new instructions
            self.show_instructions('instructions-3.gif', 2)

            ## do XAB tranfer phase
            testitems = self.get_transfer_set()
            indexes = range(len(testitems))
            
            for bl in range(N_TEST_BLOCKS): 
                self.block += 0
                shuffle(indexes)
                for ind in indexes:
                    if randint(0,2)==0:
                        self.show_face_xab(testitems[ind][0][0], testitems[ind][0][1], trialtypes["xab-pretest"], testitems[ind][1], "Please study this face", "Which face matches the previous one?", 500,500, 1500)
                    else:
                        self.show_face_xab(testitems[ind][0][1], testitems[ind][0][0], trialtypes["xab-pretest"], testitems[ind][1], "Please study this face", "Which face matches the previous one?", 500,500, 1500)
                
                if bl != N_TEST_BLOCKS-1:
                    self.show_break("break.gif", 10000)
    

        if TRAINING:
            ## show instructions - wait for keypress
            self.show_instructions('instructions-1b.gif', 2)

            # choose a random x and y
            if self.cond == NOCLUSTER:
                if self.rule == HOR_RULE:
                    trainingitems = [
                        "0101.gif", "0102.gif", "0103.gif", "0104.gif", "0107.gif", "0108.gif", "0109.gif", "0110.gif",
                        "0201.gif", "0202.gif", "0203.gif", "0204.gif", "0207.gif", "0208.gif", "0209.gif", "0210.gif",
                        "0301.gif", "0302.gif", "0303.gif", "0304.gif", "0307.gif", "0308.gif", "0309.gif", "0310.gif",
                        "0401.gif", "0402.gif", "0403.gif", "0404.gif", "0407.gif", "0408.gif", "0409.gif", "0410.gif",
                        "0501.gif", "0502.gif", "0503.gif", "0504.gif", "0507.gif", "0508.gif", "0509.gif", "0510.gif",
                        "0601.gif", "0602.gif", "0603.gif", "0604.gif", "0607.gif", "0608.gif", "0609.gif", "0610.gif",
                        "0701.gif", "0702.gif", "0703.gif", "0704.gif", "0707.gif", "0708.gif", "0709.gif", "0710.gif",
                        "0801.gif", "0802.gif", "0803.gif", "0804.gif", "0807.gif", "0808.gif", "0809.gif", "0810.gif",
                        "0901.gif", "0902.gif", "0903.gif", "0904.gif", "0907.gif", "0908.gif", "0909.gif", "0910.gif",
                        "1001.gif", "1002.gif", "1003.gif", "1004.gif", "1007.gif", "1008.gif", "1009.gif", "1010.gif"
                        ]
                elif self.rule == VERT_RULE:
                    trainingitems = [
                        "0101.gif", "0102.gif", "0103.gif", "0104.gif", "0105.gif", "0106.gif", "0107.gif", "0108.gif", "0109.gif", "0110.gif",
                        "0201.gif", "0202.gif", "0203.gif", "0204.gif", "0205.gif", "0206.gif", "0207.gif", "0208.gif", "0209.gif", "0210.gif",
                        "0301.gif", "0302.gif", "0303.gif", "0304.gif", "0305.gif", "0306.gif", "0307.gif", "0308.gif", "0309.gif", "0310.gif",
                        "0401.gif", "0402.gif", "0403.gif", "0404.gif", "0405.gif", "0406.gif", "0407.gif", "0408.gif", "0409.gif", "0410.gif",
                        "0701.gif", "0702.gif", "0703.gif", "0704.gif", "0705.gif", "0706.gif", "0707.gif", "0708.gif", "0709.gif", "0710.gif",
                        "0801.gif", "0802.gif", "0803.gif", "0804.gif", "0805.gif", "0806.gif", "0807.gif", "0808.gif", "0809.gif", "0810.gif",
                        "0901.gif", "0902.gif", "0903.gif", "0904.gif", "0905.gif", "0906.gif", "0907.gif", "0908.gif", "0909.gif", "0910.gif",
                        "1001.gif", "1002.gif", "1003.gif", "1004.gif", "1005.gif", "1006.gif", "1007.gif", "1008.gif", "1009.gif", "1010.gif"
                        ]
            else:
                trainingitems = [
                    "0101.gif", "0102.gif", "0103.gif", "0104.gif", "0107.gif", "0108.gif", "0109.gif", "0110.gif",
                    "0201.gif", "0202.gif", "0203.gif", "0204.gif", "0207.gif", "0208.gif", "0209.gif", "0210.gif",
                    "0301.gif", "0302.gif", "0303.gif", "0304.gif", "0307.gif", "0308.gif", "0309.gif", "0310.gif",
                    "0401.gif", "0402.gif", "0403.gif", "0404.gif", "0407.gif", "0408.gif", "0409.gif", "0410.gif",
                    "0701.gif", "0702.gif", "0703.gif", "0704.gif", "0707.gif", "0708.gif", "0709.gif", "0710.gif",
                    "0801.gif", "0802.gif", "0803.gif", "0804.gif", "0807.gif", "0808.gif", "0809.gif", "0810.gif",
                    "0901.gif", "0902.gif", "0903.gif", "0904.gif", "0907.gif", "0908.gif", "0909.gif", "0910.gif",
                    "1001.gif", "1002.gif", "1003.gif", "1004.gif", "1007.gif", "1008.gif", "1009.gif", "1010.gif"
                    ]

            ## do XAB trials
            testitems = self.get_transfer_set()
            indexes = range(len(testitems))
            
            for bl in range(NBLOCKS):
                self.block +=1
                shuffle(trainingitems)
                #shuffle(indexes)
                catindex = 0
                xabindex = 0
                for tr in range(LEARNBLOCKTRIALS):
                    print tr
                
                    if tr%15 == 0:
                        orderset = [0,0,0,0,0,0,0,0,1,1,1,1,1,1,1]
                        discset = [0,1,2,3,4,5,6]
                        inset = [[0,1,2,3,4,5,6,7],[0,1,2,3,4,5,6,7],[0,1,2,3,4,5,6,7],[0,1,2,3,4,5,6,7],[0,1,2,3,4,5,6,7],[0,1,2,3,4,5,6,7],[0,1,2,3,4,5,6,7]]
                        map(lambda x: shuffle(x), inset)
                        shuffle(orderset)
                        shuffle(discset)
                    
                    if orderset[tr%15]==0:
                        # do cat trial
                        filename = trainingitems[catindex%len(trainingitems)]
                        catindex+=1
                        myx=int(filename[0:2])
                        myy=int(filename[2:4])
                        #(myx, myy) = (xcoord[randint(0,len(xcoord))],ycoord[randint(0,len(ycoord))])
                        #filename = "%02d%02d.gif" % (myx, myy)
                        #print filename
                    
                        # what is the correct category for the item?
                        if self.rule == HOR_RULE:
                            if self.order == AB:
                                if myx < 5:
                                    print "category A"
                                    cans = A
                                else: 
                                    print "category B"
                                    cans = B
                            elif self.order == BA:
                                if myx < 5:
                                    print "category B"
                                    cans = B
                                else:
                                    print "category A"
                                    cans = A
                        elif self.rule == VERT_RULE:
                            if self.order == AB:
                                if myy < 5:
                                    print "category A"
                                    cans = A
                                else: 
                                    print "category B"
                                    cans = B
                            elif self.order == BA:
                                if myy < 5:
                                    print "category B"
                                    cans = B
                                else:
                                    print "category A"
                                    cans = A
                                 
                        self.show_face_respond(filename, cans,  "Please study this face", "Did that person belong to club 'Q' or 'P'?", "Press the 'Q' or 'P' key to record your response.",500,300,2000,1000)
                    
                    else:
                        # do xab trial
                        print discset
                        print discset[0]
                        inda = discset[0]
                        discset = discset[1:]
                        print discset
                    
                        print inset[inda]
                        print inset[inda][0]
                        indb=inset[inda][0]
                        inset[inda] = inset[inda][1:]
                        print inset[inda]
                    
                        #ind = indexes[xabindex%len(indexes)]
                        ind = inda*8+indb
                    
                        print "MY INDEX IS, ", ind
                        print "MY TYPE IS, ", testitems[ind][1]
                        #xabindex+=1
                        if randint(0,2)==0:
                            self.show_face_xab(testitems[ind][0][0], testitems[ind][0][1], trialtypes["xab-traintest"], testitems[ind][1], "Please study this face", "Which face matches the previous one?", 500,300, 2000)
                        else:
                            self.show_face_xab(testitems[ind][0][1], testitems[ind][0][0], trialtypes["xab-traintest"], testitems[ind][1], "Please study this face", "Which face matches the previous one?", 500,300, 2000)
                
                     
                if bl != NBLOCKS-1:
                    self.show_break("break.gif", 8000)

        if POSTTEST:
            if self.cond == VERBALTASK or self.cond == SPATIALTASK:
                ## break with new instructions
                self.show_instructions('instructions-2b.gif', 2) 
                self.show_instructions('instructions-2c.gif', 2)                
            else:
                ## break with new instructions
                self.show_instructions('instructions-2.gif', 2)


            ## do XAB tranfer phase
            testitems = self.get_transfer_set()
            indexes = range(len(testitems))
            for bl in range(N_TEST_BLOCKS): 
                self.block +=1
                blocktrial = 0
                shuffle(indexes)
                for ind in indexes:
                    if blocktrial%8 == 0:
                        # show test stimulus
                        if self.cond == VERBALTASK:
                            correctanswer = self.show_verbal_task(8000, 3000)
                        elif self.cond == SPATIALTASK:
                            correctanswer = self.show_spatial_task(8000, 3000)
                    
                    if randint(0,2)==0:
                        self.show_face_xab(testitems[ind][0][0], testitems[ind][0][1], trialtypes["xab-test"], testitems[ind][1], "Please study this face", "Which face matches the previous one?", 500,300, 1500)
                    else:
                        self.show_face_xab(testitems[ind][0][1], testitems[ind][0][0], trialtypes["xab-test"], testitems[ind][1], "Please study this face", "Which face matches the previous one?", 500,300, 1500)
                    
                    if blocktrial%8 == 7:
                        # show test stimulus
                        if self.cond == VERBALTASK:
                            self.test_verbal_task(correctanswer, "Which item matches the one you last memorized?", 1500)
                        elif self.cond == SPATIALTASK:
                            self.test_spatial_task(correctanswer, "Which item matches the one you last memorized?", 1500)
                    blocktrial+=1
                
                if bl != N_TEST_BLOCKS-1:
                    self.show_break("break.gif", 10000)
        
        self.show_thanks()
        
        
    ###########################################################
    # get_transfer_set
    ###########################################################
    def get_transfer_set(self):
        # defined in terms of category boundary
        if self.rule == VERT_RULE:
            type1 = WITHIN_CLUSTER_HORIZ
            type2 = WITHIN_CLUSTER_VERT
            type3 = WITHIN_CLUSTER_DIAG
            type4 = BETWEEN_CLUSTER_VERT
            type5 = BETWEEN_CLUSTER_DIAG
            type6 = BETWEEN_CATEGORY_HORIZ
            type7 = BETWEEN_CATEGORY_DIAG
            
        elif self.rule == HOR_RULE:
            type1 = WITHIN_CLUSTER_VERT
            type2 = WITHIN_CLUSTER_HORIZ
            type3 = WITHIN_CLUSTER_DIAG
            type4 = BETWEEN_CATEGORY_HORIZ
            type5 = BETWEEN_CATEGORY_DIAG
            type6 = BETWEEN_CLUSTER_VERT
            type7 = BETWEEN_CLUSTER_DIAG

        #============================== 
        #Within Cluster Horizontal
        comparisonset = [
            [["0101.gif","0104.gif"], type1],
            [["0401.gif","0404.gif"], type1],
            [["0701.gif","0704.gif"], type1],
            [["1001.gif","1004.gif"], type1],
            [["0107.gif","0110.gif"], type1],
            [["0407.gif","0410.gif"], type1],
            [["0707.gif","0710.gif"], type1],
            [["1007.gif","1010.gif"], type1],
            
            #Within Cluster Vertical    
            [["0101.gif","0401.gif"], type2],
            [["0104.gif","0404.gif"], type2],
            [["0701.gif","1001.gif"], type2],
            [["0704.gif","1004.gif"], type2],
            [["0107.gif","0407.gif"], type2],
            [["0110.gif","0410.gif"], type2],
            [["0707.gif","1007.gif"], type2],
            [["0710.gif","1010.gif"], type2],
            
            
            #Within Cluster Diagonal    
            [["0101.gif","0404.gif"], type3],
            [["0104.gif","0401.gif"], type3],
            [["0701.gif","1004.gif"], type3],
            [["0704.gif","1001.gif"], type3],
            [["0107.gif","0410.gif"], type3],
            [["0110.gif","0407.gif"], type3],
            [["0707.gif","1010.gif"], type3],
            [["0710.gif","1007.gif"], type3],
            
            #==============================
            #Between Cluster Vertical   
            [["0401.gif","0701.gif"], type4],
            [["0402.gif","0702.gif"], type4],
            [["0403.gif","0703.gif"], type4],
            [["0404.gif","0704.gif"], type4],
            [["0407.gif","0707.gif"], type4],
            [["0408.gif","0708.gif"], type4],
            [["0409.gif","0709.gif"], type4],
            [["0410.gif","0710.gif"], type4],
            
            #Between Cluster Diagonal   
            [["0401.gif","0704.gif"], type5],
            [["0404.gif","0701.gif"], type5],
            [["0407.gif","0710.gif"], type5],
            [["0410.gif","0707.gif"], type5],
            [["0401.gif","0704.gif"], type5],
            [["0404.gif","0701.gif"], type5],
            [["0407.gif","0710.gif"], type5],
            [["0410.gif","0707.gif"], type5],
            
            #==============================
            #Between Category Horizontal    
            [["0104.gif","0107.gif"], type6],
            [["0204.gif","0207.gif"], type6],
            [["0304.gif","0307.gif"], type6],
            [["0404.gif","0407.gif"], type6],
            [["0704.gif","0707.gif"], type6],
            [["0804.gif","0807.gif"], type6],
            [["0904.gif","0907.gif"], type6],
            [["1004.gif","1007.gif"], type6],
            
            #Between Category Horizontal    
            [["0104.gif","0407.gif"], type7],
            [["0404.gif","0107.gif"], type7],
            [["0704.gif","1007.gif"], type7],
            [["1004.gif","0707.gif"], type7],
            [["0104.gif","0407.gif"], type7],
            [["0404.gif","0107.gif"], type7],
            [["0704.gif","1007.gif"], type7],
            [["1004.gif","0707.gif"], type7]
        ]
        
        return comparisonset

    ###########################################################
    # load_image
    ###########################################################
    def load_image(self, fullname, colorkey=None):
        try:
            image = pygame.image.load(fullname)
        except pygame.error, message:
            print "Can't load image:", fullname
            raise SystemExit, message
        image = image.convert()
        #if colorkey is not None:
        #   if colorkey is -1:
        #       colorkey = image.get_at((0,0))
        #   image.set_colorkey(colorkey, RLEACCEL)
        #colorkey = image.get_at((0,0))
        #image.set_colorkey(colorkey, RLEACCEL) 
        return image
        
    ###########################################################
    # get_text_image
    ###########################################################
    def get_text_image(self, font, message, fontcolor, bg):
        base = font.render(message, 1, fontcolor)
        size = base.get_width(), base.get_height()
        img = pygame.Surface(size, 16)
        img = img.convert()
        img.fill(bg)
        img.blit(base, (0, 0))
        return img
    
    ###########################################################
    # load_all_resources
    ###########################################################
    def load_all_resources(self, img_directory):
        # drop all . files
        files = filter(lambda x: x[0] != '.', os.listdir(os.path.join(os.curdir, img_directory)))
        files = filter(lambda x: x != 'Thumbs.db', files)
        full_path_files = map( lambda x: os.path.join(os.curdir, img_directory, x), files)
        images = map(lambda x: self.load_image(x), full_path_files)
        self.resources = {}
        for i in range(len(files)): self.resources[files[i]]=images[i]
    
    ###########################################################
    # show_image
    ###########################################################
    def show_image(self, imagename, bgcolor, xoffset, yoffset):
        size = self.screen.get_size()
        background = pygame.Surface(size)
        background = background.convert()
        background.fill(bgcolor)
        
        image = self.resources[imagename]
        image_rect = image.get_rect()
        image_rect.centerx = background.get_rect().centerx + xoffset
        image_rect.centery = background.get_rect().centery + yoffset
        
        background.blit(image,image_rect)
        return background
                        
                        
    ###########################################################
    # show_image_add
    ###########################################################
    def show_image_add(self, background, imagename, xoffset, yoffset):
        size = self.screen.get_size()
        
        image = self.resources[imagename]
        image_rect = image.get_rect()
        image_rect.centerx = background.get_rect().centerx + xoffset
        image_rect.centery = background.get_rect().centery + yoffset
        
        background.blit(image,image_rect)
        return background
        
    ###########################################################
    # show_thanks
    ###########################################################
    def show_thanks(self):
    
        global experimentname
        background = self.show_image('thanks.gif',black, 0, 0)
        
        # show subject number and experment name
#       exp_text = "EXPERIMENT NAME: %s" % experimentname
#       text = self.get_text_image(pygame.font.Font(None, 32), exp_text, white, ltgrey)
#       textpos = text.get_rect()
#       textpos.centerx = background.get_rect().centerx
#       textpos.centery = background.get_rect().centery + 200
#       background.blit(text, textpos)
#       
#       subj_text = "SUBJECT NUMBER: %s" % self.subj
#       text = self.get_text_image(pygame.font.Font(None, 32), subj_text, white, ltgrey)
#       textpos = text.get_rect()
#       textpos.centerx = background.get_rect().centerx
#       textpos.centery = background.get_rect().centery + 250
#       background.blit(text, textpos)
        
        self.screen.blit(background, (0,0))
        pygame.display.flip()
        
        while 1:
            res = self.get_response()

    ###########################################################
    # show_break
    ###########################################################
    def show_break(self, filename, iti):
        background = self.show_image(filename, black, 0, 0)     
        self.screen.blit(background, (0,0))
        pygame.display.flip()
        self.escapable_sleep(iti)
        # 1. output subj number, condition number, trial number, trialtype,  res, rt, pattern type, pattern, filename, 
        self.output_trial([self.subj, self.cond, trialtypes["break"], filename])
        
        
        background = self.show_image(filename, black, 0, 0) 
        exp_text = "please press the N key to continue"
        text = self.get_text_image(pygame.font.Font(None, 32), exp_text, white, black)
        textpos = text.get_rect()
        textpos.centerx = background.get_rect().centerx
        textpos.centery = background.get_rect().centery + 235
        background.blit(text, textpos)
        self.screen.blit(background, (0,0))
        pygame.display.flip()
        
        while 1:
            res = self.get_response()
            if (res == 'n'):
                break        
        
    ###########################################################
    # show_instructions
    ###########################################################
    def show_instructions(self, filename, npress):
        background = self.show_image(filename, black, 0, 0)     
        self.screen.blit(background, (0,0))
        pygame.display.flip()

        time_stamp = pygame.time.get_ticks()
        for i in range(npress):
            
            if i == (npress-1)  and npress != 1:
                exp_text = "once more"
                text = self.get_text_image(pygame.font.Font(None, 26), exp_text, white, black)
                textpos = text.get_rect()
                textpos.centerx = background.get_rect().centerx
                textpos.centery = background.get_rect().centery + 235
                background.blit(text, textpos)
                self.screen.blit(background, (0,0))
                pygame.display.flip()
    
            while 1:
                res = self.get_response()
                if (res == 'n'):
                    break
        
        rt = pygame.time.get_ticks() - time_stamp
        # output results
        # 1. output subj number, condition number, trial number, trialtype,  rt, filename 
        self.output_trial([self.subj, self.cond, trialtypes["instruction"], rt, filename])
            
    ###########################################################
    # output_trial
    ###########################################################
    def output_trial(self, myline):
        # format: output 1 subj number, 2 condition number, 3 trial number, 4 block, 5 res, 6 rt, 7 pattern type, 8 pattern class, 9 filename
        ##print myline
        
        # general information
        ##print "subj #:\t ", myline[0]
        ##print "cond #:\t ", myline[1]
        ##print "trial #:\t ", myline[2]
        ##print "block:\t ", myline[3]
        ##print "resp: yes/no ", myline[4]
        ##print "rt: ", myline[5]
        ##print "pattern type: ", myline[6]
        ##print "pattern class: ", myline[7]
        ##print "filename : ", myline[8]
        
        for i in myline:
            self.datafile.write(str(i)+' ')
            
        self.datafile.write('\n')
        self.datafile.flush()
        


    ###########################################################
    # get_response_and_rt
    ###########################################################
    def get_response_and_rt(self):
        time_stamp = pygame.time.get_ticks()
        while 1:
            res = self.get_response()
            if (res == 'Q' or res=='q'):
                res = A
                break
            elif (res == 'P' or res=='p'):
                res = B
                break
        
        rt = pygame.time.get_ticks() - time_stamp
        
        return [res, rt]

    ###########################################################
    # show_face_xab
    ###########################################################
    def show_face_xab(self, a_file, b_file, trialtype, testtype, prompt, prompt2, studytime, pausetime, iti):
        
        background = self.show_image(a_file, black, 0, 0)

        if prompt != '':
            text = self.get_text_image(pygame.font.Font(None, 30), prompt, white, black)
            textpos = text.get_rect()
            textpos.centerx = background.get_rect().centerx
            textpos.centery = background.get_rect().centery - 250
            background.blit(text, textpos)

        self.screen.blit(background, (0,0))
        pygame.display.flip()
        self.escapable_sleep(studytime)
        
        
        size = self.screen.get_size()
        background = pygame.Surface(size)
        background = background.convert()
        background.fill(black)
        self.screen.blit(background, (0,0))
        pygame.display.flip()
        self.escapable_sleep(pausetime)
        
        
        size = self.screen.get_size()
        background = pygame.Surface(size)
        background = background.convert()
        background.fill(black)

        # show both side by side
        if randint(0,2) == 0:
            background = self.show_image(a_file, black, -200, 0)
            background = self.show_image_add(background, b_file, 200, 0)
            cans = A
        else:
            background = self.show_image(b_file, black, -200, 0)
            background = self.show_image_add(background, a_file, 200, 0)
            cans = B
            
        if prompt2 != '':
            text = self.get_text_image(pygame.font.Font(None, 30), prompt2, white, black)
            textpos = text.get_rect()
            textpos.centerx = background.get_rect().centerx
            textpos.centery = background.get_rect().centery - 250
            background.blit(text, textpos)

        text = self.get_text_image(pygame.font.Font(None, 30), "press 'Q' for this face", white, black)
        textpos = text.get_rect()
        textpos.centerx = background.get_rect().centerx - 200
        textpos.centery = background.get_rect().centery + 250
        background.blit(text, textpos)

        text = self.get_text_image(pygame.font.Font(None, 30), "press 'P' for this face", white, black)
        textpos = text.get_rect()
        textpos.centerx = background.get_rect().centerx + 200
        textpos.centery = background.get_rect().centery + 250
        background.blit(text, textpos)

            
        self.screen.blit(background, (0,0))
        pygame.display.flip()
        
        [res, rt] = self.get_response_and_rt()
        
        if(res == cans):
            hit = 1
        else:
            hit = 0
            
        # write out data
        # 1. output subj number, condition number, trial number, trialtype,  res, rt, pattern type, pattern, filename, 
        self.output_trial([self.subj, self.cond, trialtype, self.trial, self.block, testtype, res, cans, hit, rt, a_file, b_file])
        
        
        size = self.screen.get_size()
        background = pygame.Surface(size)
        background = background.convert()
        background.fill(black)
        self.screen.blit(background, (0,0))
        pygame.display.flip()
        self.escapable_sleep(iti)
        self.trial+=1


    ###########################################################
    # show_verbal_task
    ###########################################################
    def show_verbal_task(self, studytime, iti):
        
        # please study this face prompt
        size = self.screen.get_size()
        background = pygame.Surface(size)
        background = background.convert()
        background.fill(black)
        
        # draw prompt
        prompta = "Memorize:"
        
        if prompta != '':
            text = self.get_text_image(pygame.font.Font(None, 30), prompta, white, black)
            textpos = text.get_rect()
            textpos.centerx = background.get_rect().centerx
            textpos.centery = background.get_rect().centery - 250
            background.blit(text, textpos)
     
        # generate study string
        studystring = ''
        for i in range(8):
            studystring += str(randint(0,10))
        
        # draw study string
        if  studystring != '':
            text = self.get_text_image(pygame.font.Font(None, 95), studystring, white, black)
            textpos = text.get_rect()
            textpos.centerx = background.get_rect().centerx
            textpos.centery = background.get_rect().centery - 0
            background.blit(text, textpos)
        
        self.screen.blit(background, (0,0))
        pygame.display.flip()
        self.escapable_sleep(studytime)
        
        # write out data
        # 1. output subj number, condition number, trial number, trialtype,  res, rt, pattern type, pattern, filename, 
        self.output_trial([self.subj, self.cond, trialtypes["dualtaskstudy"], self.trial, self.block, 1, -1, -1, -1, -1, -1, studystring])
        
        size = self.screen.get_size()
        background = pygame.Surface(size)
        background = background.convert()
        background.fill(black)
        
        self.screen.blit(background, (0,0))
        pygame.display.flip()
        self.escapable_sleep(iti)
        self.trial+=1
        
        return studystring
        
        
    ###########################################################
    # test_verbal_task
    ###########################################################
    def test_verbal_task(self, correctanswer, prompt, iti):
        
        flip = randint(1,len(correctanswer)+1)
        print "FLIPPING BIT", flip
        newbit = randint(0,10)
        while newbit == correctanswer[flip-1]:
            newbit = randint(0,10)
        foilstring = correctanswer[0:flip-1] + str(newbit) + correctanswer[flip:]
                       
        # please study this face prompt
        size = self.screen.get_size()
        background = pygame.Surface(size)
        background = background.convert()
        background.fill(black)
        
        # draw prompt
        if prompt != '':
            text = self.get_text_image(pygame.font.Font(None, 30), prompt, white, black)
            textpos = text.get_rect()
            textpos.centerx = background.get_rect().centerx
            textpos.centery = background.get_rect().centery - 275
            background.blit(text, textpos)
        
        if randint(0,2)==0:
            left = correctanswer
            right = foilstring
            cans = 0
        else:
            left = foilstring
            right = correctanswer
            cans = 1
        
        # draw study string
        if left != '':
            text = self.get_text_image(pygame.font.Font(None, 95), left, white, black)
            textpos = text.get_rect()
            textpos.centerx = background.get_rect().centerx - 250
            textpos.centery = background.get_rect().centery - 0
            background.blit(text, textpos)

            text = self.get_text_image(pygame.font.Font(None, 30), 'Press Q for this one', white, black)
            textpos = text.get_rect()
            textpos.centerx = background.get_rect().centerx - 250
            textpos.centery = background.get_rect().centery + 75
            background.blit(text, textpos)
            
        # draw study string
        if right != '':
            text = self.get_text_image(pygame.font.Font(None, 95), right, white, black)
            textpos = text.get_rect()
            textpos.centerx = background.get_rect().centerx + 250
            textpos.centery = background.get_rect().centery - 0
            background.blit(text, textpos)

            text = self.get_text_image(pygame.font.Font(None, 30), 'Press P for this one', white, black)
            textpos = text.get_rect()
            textpos.centerx = background.get_rect().centerx + 250
            textpos.centery = background.get_rect().centery + 75
            background.blit(text, textpos)
        
        self.screen.blit(background, (0,0))
        pygame.display.flip()
        
        [res, rt] = self.get_response_and_rt()
        
        if(res == cans):
            hit = 1
        else:
            hit = 0
        
        # write out data
        # 1. output subj number, condition number, trial number, trialtype,  res, rt, pattern type, pattern, filename, 
        self.output_trial([self.subj, self.cond, trialtypes["dualtasktest"], self.trial, self.block, 1, res, cans, hit, rt, correctanswer, foilstring, left, right])
       
        size = self.screen.get_size()
        background = pygame.Surface(size)
        background = background.convert()
        background.fill(black)
        
        self.screen.blit(background, (0,0))
        pygame.display.flip()
        self.escapable_sleep(iti)
        self.trial+=1
        
    ###########################################################
    # draw_spatial_grid
    ###########################################################
    def show_spatial_grid(self, surface, x, y, pattern):
        myrect = Rect(0,0,300,300)
        myrect.centerx = x
        myrect.centery = y
        pygame.draw.rect(surface, ltgrey, myrect, 2)
        
        print pattern
        ind = 0
        for i in range(4):
            for j in range(4):
                myrect = Rect(x-145+74*i,y-145+74*j,68,68)
                if pattern[ind]=='1':
                    pygame.draw.rect(surface, white, myrect, 0)
                else:
                    pygame.draw.rect(surface, black, myrect, 0)
                ind+=1
        
        
    ###########################################################
    # show_spatial_task
    ###########################################################
    def show_spatial_task(self, studytime, iti):
        
        # please study this face prompt
        size = self.screen.get_size()
        background = pygame.Surface(size)
        background = background.convert()
        background.fill(black)
        
        # draw prompt
        prompta = "Memorize:"
        
        if prompta != '':
            text = self.get_text_image(pygame.font.Font(None, 30), prompta, white, black)
            textpos = text.get_rect()
            textpos.centerx = background.get_rect().centerx
            textpos.centery = background.get_rect().centery - 250
            background.blit(text, textpos)
        
        # generate study string
        studystring = ''
        for i in range(16):
            studystring += str(randint(0,2))
        
        # draw study string
        if studystring != '':
            cx = background.get_rect().centerx
            cy = background.get_rect().centery
            self.show_spatial_grid(background, cx, cy, studystring)
        
        self.screen.blit(background, (0,0))
        pygame.display.flip()
        self.escapable_sleep(studytime)
        
        # write out data
        # 1. output subj number, condition number, trial number, trialtype,  res, rt, pattern type, pattern, filename, 
        self.output_trial([self.subj, self.cond, trialtypes["dualtaskstudy"], self.trial, self.block, 1, -1, -1, -1, -1, -1, studystring])
        
        size = self.screen.get_size()
        background = pygame.Surface(size)
        background = background.convert()
        background.fill(black)
        
        self.screen.blit(background, (0,0))
        pygame.display.flip()
        self.escapable_sleep(iti)
        self.trial+=1
        
        return studystring    

    ###########################################################
    # test_spatial_task
    ###########################################################
    def test_spatial_task(self, correctanswer, prompt, iti):
        
        flip = randint(1,len(correctanswer)+1)
        print "FLIPPING BIT", flip
        newbit = randint(0,2)
        while newbit == correctanswer[flip-1]:
            newbit = randint(0,2)
        foilstring = correctanswer[0:flip-1] + str(newbit) + correctanswer[flip:]
                       
        # please study this face prompt
        size = self.screen.get_size()
        background = pygame.Surface(size)
        background = background.convert()
        background.fill(black)
        
        # draw prompt
        if prompt != '':
            text = self.get_text_image(pygame.font.Font(None, 30), prompt, white, black)
            textpos = text.get_rect()
            textpos.centerx = background.get_rect().centerx
            textpos.centery = background.get_rect().centery - 275
            background.blit(text, textpos)
        
        if randint(0,2)==0:
            left = correctanswer
            right = foilstring
            cans = 0
        else:
            left = foilstring
            right = correctanswer
            cans = 1
        
        # draw study string
        if left != '':
            cx = background.get_rect().centerx - 300
            cy = background.get_rect().centery
            self.show_spatial_grid(background, cx, cy, left)
            
            text = self.get_text_image(pygame.font.Font(None, 30), 'Press Q for this one', white, black)
            textpos = text.get_rect()
            textpos.centerx = background.get_rect().centerx - 300
            textpos.centery = background.get_rect().centery + 200
            background.blit(text, textpos)
            
        # draw study string
        if right != '':
            cx = background.get_rect().centerx + 300
            cy = background.get_rect().centery
            self.show_spatial_grid(background, cx, cy, right)
            
            text = self.get_text_image(pygame.font.Font(None, 30), 'Press P for this one', white, black)
            textpos = text.get_rect()
            textpos.centerx = background.get_rect().centerx + 300
            textpos.centery = background.get_rect().centery + 200
            background.blit(text, textpos)
        
        self.screen.blit(background, (0,0))
        pygame.display.flip()
        
        [res, rt] = self.get_response_and_rt()
        
        if(res == cans):
            hit = 1
        else:
            hit = 0
        
        # write out data
        # 1. output subj number, condition number, trial number, trialtype,  res, rt, pattern type, pattern, filename, 
        self.output_trial([self.subj, self.cond, trialtypes["dualtasktest"], self.trial, self.block, 1, res, cans, hit, rt, correctanswer, foilstring, left, right])
       
        size = self.screen.get_size()
        background = pygame.Surface(size)
        background = background.convert()
        background.fill(black)
        
        self.screen.blit(background, (0,0))
        pygame.display.flip()
        self.escapable_sleep(iti)
        self.trial+=1
    
    ###########################################################
    # show_face_respond
    ###########################################################
    def show_face_respond(self, fileinfo, cans, prompt, prompt2, prompt3, studytime, pausetime, assctime, iti):
    
        # please study this face prompt
        background = self.show_image(fileinfo, black, 0, 0) 
        
        if prompt != '':
            text = self.get_text_image(pygame.font.Font(None, 30), prompt, white, black)
            textpos = text.get_rect()
            textpos.centerx = background.get_rect().centerx
            textpos.centery = background.get_rect().centery - 250
            background.blit(text, textpos)

        self.screen.blit(background, (0,0))
        pygame.display.flip()
        self.escapable_sleep(studytime)
        
        
        size = self.screen.get_size()
        background = pygame.Surface(size)
        background = background.convert()
        background.fill(black)
        self.screen.blit(background, (0,0))
        pygame.display.flip()
        self.escapable_sleep(pausetime)
        
        # what this person in category A or category B?
        # display face again and feedback
        size = self.screen.get_size()
        background = pygame.Surface(size)
        background = background.convert()
        background.fill(black)
        
                
        if prompt != '':
            text = self.get_text_image(pygame.font.Font(None, 30), prompt2, white, black)
            textpos = text.get_rect()
            textpos.centerx = background.get_rect().centerx
            textpos.centery = background.get_rect().centery - 250
            background.blit(text, textpos)
        
        if prompt2 != '':
            text = self.get_text_image(pygame.font.Font(None, 24), prompt3, white, black)
            textpos = text.get_rect()
            textpos.centerx = background.get_rect().centerx
            textpos.centery = background.get_rect().centery - 225
            background.blit(text, textpos)
            
        self.screen.blit(background, (0,0))         
        pygame.display.flip()
    
        [res, rt] = self.get_response_and_rt()
        
        if(res == cans):
            hit = 1
        else:
            hit = 0
            
        # write out data
        # 1. output subj number, condition number, trial number, trialtype,  res, rt, pattern type, pattern, filename, 
        self.output_trial([self.subj, self.cond, trialtypes["training"], self.trial, self.block, 1, res, cans, hit, rt, fileinfo, 'xxxxx'])
        

        # size = self.screen.get_size()
        # background = pygame.Surface(size)
        # background = background.convert()
        # background.fill(black)
        background = self.show_image(fileinfo, black, 0, 0) 
        
        # sound??
        # show feedback
        if hit == 1:
            text = self.get_text_image(pygame.font.Font(None, 30), "CORRECT!", white, black)
            textpos = text.get_rect()
            textpos.centerx = background.get_rect().centerx
            textpos.centery = background.get_rect().centery - 250
            background.blit(text, textpos)
            
            if cans == 0:
                corrective = "This person is in club 'Q'"
            else:
                corrective = "This person is in club 'P'"
            text = self.get_text_image(pygame.font.Font(None, 24), corrective, white, black)
            textpos = text.get_rect()
            textpos.centerx = background.get_rect().centerx
            textpos.centery = background.get_rect().centery - 225
            background.blit(text, textpos)
            
        else:
            text = self.get_text_image(pygame.font.Font(None, 30), "Sorry, that is INCORRECT.", white, black)
            textpos = text.get_rect()
            textpos.centerx = background.get_rect().centerx
            textpos.centery = background.get_rect().centery - 250
            background.blit(text, textpos)
            
            if cans == 0:
                corrective = "This person is in club 'Q'"
            else:
                corrective = "This person is in club 'P'"
            text = self.get_text_image(pygame.font.Font(None, 24), corrective, white, black)
            textpos = text.get_rect()
            textpos.centerx = background.get_rect().centerx
            textpos.centery = background.get_rect().centery - 225
            background.blit(text, textpos)
                    
        self.screen.blit(background, (0,0))
        pygame.display.flip()
        self.escapable_sleep(assctime)
            
        size = self.screen.get_size()
        background = pygame.Surface(size)
        background = background.convert()
        background.fill(black)
        
        self.screen.blit(background, (0,0))
        pygame.display.flip()
        self.escapable_sleep(iti)
        self.trial+=1


                    
    ###########################################################
    # get_cond_and_subj_number
    ###########################################################
    def get_cond_and_subj_number(self, filename):
        t = []
        myfile = open(filename,'r')
        # read lines into t
        t = myfile.readlines()
        
        myfile.close()
        
        c = map(int, t)
        t = map(int, t) # convert to numbers and increment
        t[0] = (t[0]+1)%t[1]
        t[2] = t[2]+1
        f = map(lambda x: str(x) + '\n', t) # convert back to string
        
        myfile = open(filename,'w')
        myfile.seek(0)
        myfile.writelines(f)
        myfile.flush()
        myfile.close()
        return c    

    ###########################################################
    # get_cond_and_subj_number_ftp
    ###########################################################
    def get_cond_and_subj_number_ftp(self, host, username, password, filename):
        t = []
        ftp = FTP(host, username, password) # connect to ftp host
        ftp.retrlines('RETR ' + filename, t.append) # get lines
        c = t = map(int, t) # convert to numbers and increment
        t[0] = (t[0]+1)%t[1]
        t[2] = t[2]+1
        f = map(lambda x: str(x) + '\n', t) # convert back to string
        myfile = tempfile.TemporaryFile()
        myfile.writelines(f)
        myfile.seek(0) # rewind to the beginning of the file
        ftp.storlines('STOR ' + filename, myfile)
        myfile.close() # close deletes the tmpfile
        return c
        
    ###########################################################
    # upload_data
    ###########################################################
    def upload_data(self, host, username, password, filename, netfilename):
        myfile = open(filename)
        ftp = FTP(host, username, password) # connect to ftp host
        ftp.storlines('STOR ' + netfilename, myfile)
        myfile.close() # close

    ###########################################################
    # get_response
    ###########################################################
    def get_response(self):
        pygame.event.clear()
        if pygame.key.get_pressed()[K_LSHIFT] and pygame.key.get_pressed()[K_BACKQUOTE]:
            self.on_exit()
        while 1:
            event = pygame.event.poll()
            if event.type == KEYDOWN:
                resp = pygame.key.name(event.key)
                if (resp > 96 and resp < 123):
                    resp -= 40
                if (resp == '[1]' or resp=='[2]' or resp=='[3]' or resp=='[4]' or resp=='[5]'):
                    resp = resp[1]
                return resp     
                
    ###########################################################
    # escapable_sleep
    ###########################################################
    def escapable_sleep(self, pause):
        waittime = 0    
        time_stamp = pygame.time.get_ticks()
        while waittime < pause:
            pygame.event.clear()
            if pygame.key.get_pressed()[K_LSHIFT] and pygame.key.get_pressed()[K_0]:
                self.on_exit()
            waittime = pygame.time.get_ticks() - time_stamp


    ###########################################################
    # on_exit
    ###########################################################
    def on_exit(self):
        self.datafile.flush()
        self.datafile.close()
        exit()
        raise SystemExit
    
###########################################################
# main
###########################################################
def main():
    
    experiment = Experiment()
    experiment.do_regular_exp()
    
###########################################################
# let's start
###########################################################
if __name__ == '__main__':
    main()
