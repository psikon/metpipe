import subprocess
from bin.misc import Helper

class Assembly:
    
    def __init__(self):
        self.helper = Helper()
        
    def __del__(self):
        pass

    def metavelvet(self,infile, threads,paramsFile):
        p = subprocess.Popen(self.helper.createArgs('./program/velvet/velveth %s %s -%s -%s -%s %s %s' % ('result/metavelvet/',
                                     self.helper.checkParameter("Assembly", "k-mer", paramsFile), 
                                     self.helper.checkParameter("Assembly", "file-format", paramsFile),
                                     self.helper.checkParameter("Assembly", "read-type", paramsFile),
                                     self.helper.checkParameter("Assembly", "file-layout", paramsFile),
                                     ' '.join(str(i) for i in (infile)),
                                     self.helper.checkParameter("Assembly", "velveth-option", paramsFile))))
        p.wait()
        p = subprocess.Popen(self.helper.createArgs('./program/velvet/velvetg %s %s %s' % ('result/metavelvet/', '-exp_cov auto',
                                    self.helper.checkParameter("Assembly", "velvetg-option", paramsFile))))
        p.wait()
        p = subprocess.Popen(self.helper.createArgs('./program/metavelvet/meta-velvetg %s %s' % ('result/metavelvet/',
                                    self.helper.checkParameter("Assembly", "metavelvet-option", paramsFile))))
        p.wait()