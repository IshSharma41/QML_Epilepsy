%% Setup
clear; clc;

% Add required toolboxes
addpath(genpath('C:/Users/ishsh/OneDrive/Desktop/QML_Project/src/toolboxes/fieldtrip')); ft_defaults;
addpath('C:/Users/ishsh/OneDrive/Desktop/QML_Project/src/toolboxes/eeglab'); eeglab;

% Input/output paths
input_path  = 'C:/Users/ishsh/OneDrive/Desktop/QML_Project/data/raw/eeg_seizeit2/';
output_path = 'C:/Users/ishsh/OneDrive/Desktop/QML_Project/data/processed/eeg_seizeit2/derivatives/cleaned_epochs/';
log_file    = fullfile(output_path, 'preprocessing_log.txt');
fID = fopen(log_file, 'w');

% Subject list
subs = dir(fullfile(input_path, 'sub-*'));

for s = 1:length(subs)
    subject = subs(s).name;
    fprintf('\n[Processing %s]\n', subject); fprintf(fID, '\n[Processing %s]\n', subject);
    
    run_files = dir(fullfile(input_path, subject, 'ses-01', 'eeg', '*_eeg.edf'));

    for r = 1:length(run_files)
        try
            run_file = run_files(r).name;
            [~, run_id, ~] = fileparts(run_file);
            fprintf('[%s] %s\n', subject, run_id); fprintf(fID, '[%s] %s\n', subject, run_id);

            %% Load raw data
            cfg = [];
            cfg.dataset = fullfile(run_files(r).folder, run_file);
            cfg.continuous = 'yes';
            cfg.channel = 'all';
            data_raw = ft_preprocessing(cfg);

            if numel(data_raw.label) < 4
                fprintf('[%s] Skipping ICA: <4 channels\n', run_id); fprintf(fID, '[%s] Skipping ICA: <4 channels\n', run_id);
                continue;
            end

            %% Preprocessing
            cfg = [];
            cfg.demean = 'yes';
            cfg.detrend = 'yes';
            data = ft_preprocessing(cfg, data_raw);

            %% ICA
            cfg = [];
            cfg.method = 'runica';
            cfg.pca = min(20, numel(data.label));  % fix PCA errors
            comp = ft_componentanalysis(cfg, data);

            %% Reject artifacts (placeholder logic)
            bad_components = [];
            cfg = [];
            cfg.component = bad_components;
            data_clean = ft_rejectcomponent(cfg, comp, data);

            %% Convert to EEGLAB
            eeglab_data = eeg_emptyset();
            eeglab_data = pop_importdata('dataformat', 'array', 'data', cat(2, data_clean.trial{:}), ...
                                         'srate', data_clean.fsample, 'chanlocs', data_clean.label);
            eeglab_data.setname = run_id;
            eeglab_data = eeg_checkset(eeglab_data);

            % Save .set (no .fdt)
            out_dir = fullfile(output_path, subject, 'ses-t1', 'eeg');
            if ~exist(out_dir, 'dir'), mkdir(out_dir); end
            eeglab_data = pop_saveset(eeglab_data, 'filename', [run_id '.set'], 'filepath', out_dir);

            %% Save JSON
            json_file = fullfile(out_dir, [run_id '.json']);
            json_data = struct('TaskName', 'szMonitoring', 'SamplingFrequency', data_clean.fsample, ...
                               'EEGReference', 'average', 'PowerLineFrequency', 50);
            jsonwrite(json_file, json_data);

            %% Save channels.tsv
            tsv_file = fullfile(out_dir, [run_id '_channels.tsv']);
            fid = fopen(tsv_file, 'w');
            fprintf(fid, 'name\ttype\tunits\tsampling_frequency\tstatus\n');
            for i = 1:numel(data_clean.label)
                fprintf(fid, '%s\tEEG\tµV\t%.1f\tgood\n', data_clean.label{i}, data_clean.fsample);
            end
            fclose(fid);

            fprintf('[%s] DONE\n', run_id); fprintf(fID, '[%s] DONE\n', run_id);

        catch ME
            fprintf('[%s] ERROR: %s\n', run_id, ME.message); fprintf(fID, '[%s] ERROR: %s\n', run_id, ME.message);
        end
    end
end

fclose(fID);
