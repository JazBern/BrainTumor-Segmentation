%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
% A.Crimi 18.01.2012
% Histogram standardization 
%
% For details:  
% Nyul et al. 2000 "On standardizing the MR image intensity scale" 
% Magn Reson Med. 1999 ;42(6):1072-81.
%
% Crimi et al. 2013 "Semi-Automatic Classification of Lesion Patterns in Patients with Clinically Isolated Syndrome" 
% International Symposium on Biomedical Imaging: From Nano to Macro (2013) 1102-1105
%
%
% The general idea is to strech a target histogram according to the mode and
% shoulder of a template histogram.
%
% MRI data is multimodale, set the mode and shoulder to use as the
% WhiteMatter mode.
%
%Input:
% file_name_template = the Nifti files of the reference volume
% file_name_moving = the Nifti files of the image we want to normalize
% according to the template
%
% Not required:
% file_mask_template = A mask for the template file (e.g. to remove the skull)
% file_mask_moving = A mask for the moving file (e.g. to remove the skull)
%
%Output:
% nyul_hist_normalization = the normalized file_name_moving
%
% To strip the skull or to obtain a mask you can use the
% Brain Extraction Tool of FSL http://fsl.fmrib.ox.ac.uk/fsl/fslwiki/BET
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Histogram standardization of Volume
function nyul_hist_normalization()

file_name_template = '/Users/apple/Documents/IntensityNorm/Brats17_2013_25_1_t1.nii';
file_name_moving = '/Users/apple/Documents/test/Brats17_CBICA_ABM_1_t1.nii';
% Parameter for removing background values and noise outlier
%These are common sensible values
max_value =  255;
max_background_value = 1; %Assume that the background values are 0 or 1
min_noise_value =  254; %Assume that the noise has values of 254 and 255
%Histogram dependent  parameters set by users. Not critical
p1j = 0; % left shoulder mode background template
p1i = 0; % left shoulder mode background target
s1 = 1; % absolute min value 
s2 = max_value;% 255; % absolute max value
% DATA DEPENDENT PARAMENTER!!!!
% Not extremely critical but they need to be sensible, the data are
% normalized between 0 and 255,therefore these values should be always fine
%p2j = 253; %right shoulder mode foreground template, it is some sort of measurement of the variance
p2i = min_noise_value -1; % 248; %right shoulder mode foreground target, it is some sort of measurement of the variance

%Load Nifti-file
template  = load_untouch_nii(file_name_template);
%Load MASK Nifti-file
if nargin<3
    mask_template.img = ones(size(template.img));
else
    mask_template = load_untouch_nii(file_mask_template);
end

% Remove skulls
template.img = double(template.img) .*  double(mask_template.img);
 
[a b c] = size(template.img);
converted_data = reshape(template.img,1,a*b*c);      
converted_data = max_value * (converted_data - min(converted_data) )/( max(converted_data) - min(converted_data)); %Normalize between 0 and 256
converted_data_s = converted_data;
%figure;hist(converted_data,max_value); %Histogram without any processing
%Remove background and outliers
cleaned_index = find( converted_data > max_background_value & converted_data < min_noise_value );
cleaned_converted_data = converted_data(cleaned_index);%
%figure; 
%hist(cleaned_converted_data,max_value);
template_hist = hist(cleaned_converted_data,max_value); %Histogram after removing background and noise
[Y,mu_s] = max(template_hist);

% Recover the structure and save it
template.img = reshape(converted_data,a,b,c);
% Save the reference after the scaling within a range (e.g. 1-256)
save_untouch_nii(template,[ file_name_template(1:end-4) '_scaled.nii'] );

% Preprocess the target histogram
target  = load_untouch_nii(file_name_moving);
%Load MASK Nifti-file
if nargin<3
    mask_moving.img = ones(size(target.img));
else
    mask_moving = load_untouch_nii(file_mask_moving);
end
target.img = double(target.img) .* double(mask_moving.img);
[d f g] = size(target.img);
converted_data_t = reshape(target.img,1,d*f*g);
converted_data_t = max_value * (converted_data_t - min(converted_data_t) )/( max(converted_data_t) -min(converted_data_t)); %Normalize between 0 and 256
%figure; hist(converted_data_t,max_value); %Histogram without any processing
%Remove background and noise
cleaned_index = find( converted_data_t > max_background_value & converted_data_t < min_noise_value);
cleaned_converted_data_t = converted_data_t(cleaned_index);
%figure; 
%hist(cleaned_converted_data_t,max_value);
target_hist = hist(cleaned_converted_data_t,max_value); %Histogram after removing background and noise
[Y,mu_i] = max( target_hist);

%Histogram standardization
standardized_hist = zeros(size(cleaned_converted_data_t));
for (jj= 1 : length(cleaned_converted_data_t))
    if  (cleaned_converted_data_t(jj) < mu_i)      
        standardized_hist(jj) = mu_s + ( cleaned_converted_data_t(jj) - mu_i ) * ( s1 - mu_s ) / ( p1i - mu_i ) ; 
    else
        standardized_hist(jj) = mu_s + ( cleaned_converted_data_t(jj) - mu_i ) * ( s2 - mu_s ) / ( p2i - mu_i ) ; 
    end
end
%figure; hist(standardized_hist,max_value); %Histogram after standardization

% Update the data according to the scaling of the histogram
converted_data_t( cleaned_index ) = standardized_hist;
% Recover the structure and save it
target.img = reshape(converted_data_t,d,f,g);
save_untouch_nii(target,[   file_name_moving(1:end-4) '_stretched.nii'] );
