import gzip
import shutil

source_filepath = '/Users/apple/Documents/Brats17_TCIA_471_1_flair.nii.gz'
dest_filepath = '/Users/apple/Documents/Brats17_TCIA_471_1_flair.nii'
with gzip.open(source_filepath, 'rb') as f_in:
    with open(dest_filepath, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)
