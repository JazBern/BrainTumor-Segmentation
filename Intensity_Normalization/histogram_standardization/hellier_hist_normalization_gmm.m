%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
% A.Crimi 18.01.2012
% Histogram standardization Nyul et al. 2000
% GMM version of Pierre Hellier
% The general idea is to strech a target histogram according to the mode and
% shoulder of a template histogram.
%
% MRI data is multimodale, set the mode of the  shoulder to use as the
% WhiteMatter mode.
%
% NOTE : The method produces a mixture of Gaussians similar to the template
% however it introduces a lot of noise and errors. 
% A more reliable implementation requieres a better prior based on the neighbourhood,
% see Greenspan et al. 2006 for example.
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Histogram standardization of Volume
function hellier_hist_normalization_gmm( file_name_template, file_name_moving, file_mask_template, file_mask_moving )

% Parameter for removing background values and noise outlier
%These are common sensible values
max_value =  256;
max_background_value = 1; %Assume that the background values are 0 or 1
min_noise_value =  254; %Assume that lesions and noise have values of 254 and 255
%Histogram dependent  parameters set by users. Not critical
p1j = 0; % left shoulder mode background template
p1i = 0; % left shoulder mode background target
s1 = 1; % absolute min value 
s2 = max_value;%255; % absolute max value
% DATA DEPENDENT PARAMENTER!!!!
% Not extremely critical but they need to be sensible, the data are
% normalized between 0 and 255,therefore these values should be always fine
%p2j = 210; %right shoulder mode foreground template

%Load MASK Nifti-file
%Skull mask
mask_template = load_untouch_nii(file_mask_template); 
%Preprocess the template
template  = load_untouch_nii(file_name_template);
template.img = double(template.img) .*  double(mask_template.img); % Remove skull
[a b c] = size(template.img);
converted_data = reshape(template.img,1,a*b*c);      
converted_data = max_value * (converted_data - min(converted_data) )/( max(converted_data) -min(converted_data)); %Normalize range
%Save the scaled version of the reference volume
template.img = reshape(converted_data,a,b,c);
save_untouch_nii(template,[ file_name_template(1:end-4) '_scaled.nii'] );
%Remove background and artefacts from template
cleaned_index = find( converted_data > max_background_value  );
cleaned_converted_data = converted_data(cleaned_index);
figure; hist(cleaned_converted_data,max_value); %Histogram after removing background and noise
%Find the 3 main Gaussians for the reference (WM,GM,CSF)
[data_label model ]  = emgm( cleaned_converted_data, 3, 0);
mu_first_subset = round(median(cleaned_converted_data(find(data_label==1))));
mu_second_subset = round(median(cleaned_converted_data(find(data_label==2))));
mu_third_subset = round(median(cleaned_converted_data(find(data_label==3))));
% Check the order of the means, this is the order for T1
mu_csf = min([ mu_first_subset, mu_second_subset, mu_third_subset ]);
mu_wm = max([ mu_first_subset, mu_second_subset, mu_third_subset ]);
mu_gm = median([ mu_first_subset, mu_second_subset, mu_third_subset ]);

% Preprocess the target 
%Skull mask
mask_moving = load_untouch_nii(file_mask_moving); 
target  = load_untouch_nii(file_name_moving);
target.img = double(target.img) .* double(mask_moving.img); % Remove skull
[d f g] = size(target.img);
converted_data_t = double(reshape(target.img,1,d*f*g));
converted_data_t = max_value * (converted_data_t - min(converted_data_t) )/( max(converted_data_t) -min(converted_data_t)); %Normalize between 0 and 256
%Remove background and noise from target
cleaned_index = find( converted_data_t > max_background_value & converted_data_t < min_noise_value);
cleaned_converted_data_t = converted_data_t(cleaned_index);
figure; hist(cleaned_converted_data_t,max_value); %Histogram after removing background and noise
%Find the 3 main Gaussians for the target (WM,GM,CSF)
[data_label model] = emgm( cleaned_converted_data_t, 3, 0) ;
first_subset = cleaned_converted_data_t(find(data_label==1)); 
std_first = std(first_subset);
mu_i_first_subset = round(median(first_subset));
second_subset = cleaned_converted_data_t(find(data_label==2));
std_second = std(second_subset);
mu_i_second_subset = round(median(second_subset ));
third_subset =  cleaned_converted_data_t(find(data_label==3));
std_third = std(third_subset);
mu_i_third_subset = round(median(third_subset));
%Check the ordering of the means
if(mu_i_first_subset < mu_i_second_subset & mu_i_first_subset < mu_i_third_subset)
   disp('The first Gaussian is the CSF');
   mu_first_subset = mu_csf;
   
   if(mu_i_second_subset < mu_i_third_subset)
      disp('The last Gaussian is the WM');
      mu_second_subset = mu_gm;
      mu_third_subset = mu_wm;
   else
      disp('The last Gaussian is the GM');
      mu_second_subset = mu_wm;
      mu_third_subset = mu_gm;
   end
elseif (mu_i_first_subset > mu_i_second_subset & mu_i_first_subset > mu_i_third_subset)
   disp('The first Gaussian is the WM'); 
   mu_third_subset = mu_csf;
   
   if(mu_i_second_subset > mu_i_third_subset)
      disp('The last Gaussian is the GM');
      mu_second_subset = mu_gm;
      mu_third_subset = mu_wm;
   else
      disp('The last Gaussian is the CSF');
      mu_second_subset = mu_wm;
      mu_third_subset = mu_gm;
   end
else
   disp('The middle Gaussian is the CSF');
   mu_second_subset  = mu_csf;
   if(mu_i_first_subset < mu_i_third_subset)
      disp('The last Gaussian is the WM');
      mu_first_subset = mu_gm;
      mu_third_subset = mu_wm;
   else
      disp('The last Gaussian is the GM');
      mu_first_subset = mu_wm;
      mu_third_subset = mu_gm;
   end
end
mu_first_subset
mu_second_subset
mu_third_subset
mu_i_first_subset
mu_i_second_subset
mu_i_third_subset

%Histogram standardization
standardized_hist = zeros(size(first_subset));
p2i = mu_i_first_subset + std_first ;
for (jj= 1 : length(first_subset))
    if  (first_subset(jj) < mu_i_first_subset)      
        standardized_hist(jj) = mu_first_subset + ( first_subset(jj) - mu_i_first_subset )   * ( s1 - mu_first_subset ) / ( p1i - mu_i_first_subset) ; 
    else
        standardized_hist(jj) = mu_first_subset + ( first_subset(jj) - mu_i_first_subset )  * ( s2 - mu_first_subset ) / ( p2i - mu_i_first_subset ) ; 
    end
end
% Update the data according to the scaling of the histogram
converted_data_t( cleaned_index(find(data_label==1)) ) = standardized_hist;
standardized_hist = zeros(size(second_subset));
p2i = mu_i_second_subset + std_second ;
for (jj= 1 : length(second_subset))
    if  (second_subset(jj) < mu_i_second_subset)      
        standardized_hist(jj) = mu_second_subset + ( second_subset(jj) - mu_i_second_subset )  * ( s1 - mu_second_subset ) / ( p1i - mu_i_second_subset ) ; 
    else
        standardized_hist(jj) = mu_second_subset + ( second_subset(jj) - mu_i_second_subset )  * ( s2 - mu_second_subset ) / ( p2i - mu_i_second_subset ) ; 
    end
end
% Update the data according to the scaling of the histogram
converted_data_t( cleaned_index(find(data_label==2)) ) = standardized_hist;
standardized_hist = zeros(size(third_subset));
p2i = mu_i_third_subset  + std_third;
for (jj= 1 : length(third_subset))
    if  (third_subset(jj) < mu_i_third_subset)      
        standardized_hist(jj) = mu_third_subset + ( third_subset(jj) - mu_i_third_subset )  * ( s1 - mu_third_subset ) / ( p1i - mu_i_third_subset ) ; 
    else
        standardized_hist(jj) = mu_third_subset + ( third_subset(jj) - mu_i_third_subset )  * ( s2 - mu_third_subset ) / ( p2i - mu_i_third_subset ) ; 
    end
end
% Update the data according to the scaling of the histogram
converted_data_t( cleaned_index(find(data_label==3)) ) = standardized_hist;
figure; hist(converted_data_t(:),max_value); %Histogram after standardization

% Recover the structure and save it
target.img = reshape(converted_data_t,d,f,g);
save_untouch_nii(target,[ file_name_moving(1:end-4) '_stretched.nii'] );