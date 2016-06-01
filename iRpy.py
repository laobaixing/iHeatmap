import rpy2.robjects as robjects

# not only tranfer to R but also transpose at the same time
def transposeNumpyMat2R(numData):
    nc,nr = numData.shape  # R arrange data column by column
    xvec = robjects.FloatVector(numData.reshape(numData.size))  
    numDataR =  robjects.r.matrix(xvec, nrow=nr, ncol=nc)              # the numData column now is the row names of R matrix, heatmap3 use this format 
    return numDataR

def heatmap3py(numDataR, ColSideColors, annoColDicList, fileName=None, outPath=None):
    from rpy2.robjects.packages import importr    
    heatmap = importr("heatmap3")
    grdevices = importr("grDevices")                   
    from rpy2.robjects.functions import SignatureTranslatedFunction
    # explicitly translate the R argument to legal python name 
    heatmap.showLegend = SignatureTranslatedFunction(heatmap.showLegend,
                                           init_prm_translate = {'pt_bg': 'pt.bg'})       
    
    # annoName = ColSideColors.colnames
    # draw heatmap in file
    if (fileName!=None):
        grdevices.pdf(file = fileName )
        heatmap.heatmap3(numDataR,ColSideColors=ColSideColors,showRowDendro=False)
        grdevices.dev_off()
        for i in range(len(annoColDicList)):
            anno = robjects.StrVector(annoColDicList[i].keys())
            col =  robjects.StrVector(annoColDicList[i].values())            
            fileName = outPath +"/heatmapLegend" + str(i) + ".pdf"
            grdevices.pdf(file = fileName )
            heatmap.showLegend(legend= anno,col=col,cex=1.5, title="Annotation Legend: "+ColSideColors.colnames[i], pch=22, lwd = robjects.NA_Integer, pt_bg=col)
            grdevices.dev_off()        
    else:    
        # Draw heatmap in R window
        heatmap.heatmap3(numDataR,ColSideColors=ColSideColors,showRowDendro=False)      
        # Plot legends in another window
        for i in range(len(annoColDicList)):
            grdevices.dev_new()
            anno = robjects.StrVector(annoColDicList[i].keys())
            col =  robjects.StrVector(annoColDicList[i].values())
            heatmap.showLegend(legend= anno,col=col,cex=1.5, title="Annotation Legend: "+ ColSideColors.colnames[i], pch=22, lwd = robjects.NA_Integer, pt_bg=col)

