from data_load import *
from load_file import *
from contained_data import *
from space_time import *
from info_theme import *
from uml_class import *
from store_on_cloud import *


code_dataset = 0

if __name__ == "__main__":
    # Set the data source path
    all_files = get_all_files(data_source)
    datasets = []
    metadata_list = []

    # Process each file within the source
    for file_path in all_files:
        print(file_path)

        # Get identification and ingestion information
        title = os.path.basename(file_path)
        df, data_format = find_type(file_path)
        print(data_format)

        # Create identification and ingestion objects
        identification = DS_Identification(title, f"Dataset derived from {file_path}")
        ingestion = DS_Ingestion(
            dataFormat=data_format,
            fileType="file",
            updateFrequency="Unknown",
            sourceName="Data Source",
            sourceType="Public",
            sourceAddress=file_path,
        )

        # Identify the contained data into sub-classes
        spatial_parameters, temporal_parameters, cis, eis = get_contained_data(df)

        # Get spatio-temporal information
        spatialGranularity, spatialScopeLevel, spatialScope = get_space(spatial_parameters, df)
        temporalGranularity, temporalScopeLevel, temporalStart, temporalEnd = get_time(temporal_parameters, df)

        space_time = DS_Space_Time(
            space=DS_Space(
                spatialGranularity=DS_Spatial_Granularity(spatialGranularity),
                spatialScope=DS_Spatial_Scope(spatialScopeLevel, spatialScope)
            ),
            time=DS_Time(
                temporalGranularity=DS_Temporal_Granularity(temporalGranularity),
                temporalScope=DS_Temporal_Scope(temporalScopeLevel, temporalStart, temporalEnd)
            )
        )

        # Get thematic information
        min_common_theme = find_min_common_theme(eis, theme_folder_structure)
        theme = DS_Theme(themeCode=min_common_theme, themeDescription=min_common_theme)

        # Store dataset to the thematic catalogue according to its theme
        if min_common_theme:
            destination_path = os.path.join(min_common_theme.replace(" ", "_"), os.path.basename(file_path))
        else:
            destination_path = os.path.join("Uncategorized", os.path.basename(file_path))

            # 上传文件到 GCS
        save_file_to_cloud(file_path, bucket_name, destination_path)

        # Combine all data content
        data_content = spatial_parameters + temporal_parameters + cis + eis

        # Create Dataset object
        dataset = Dataset(
            identification=identification,
            ingestion=ingestion,
            space_time=space_time,
            themes=theme,
            data_content=data_content
        )
        datasets.append(dataset)

        # Extract metadata and append to the metadata list
        metadata_entry = {
            "title": identification.title,
            "description": identification.description,
            "dataFormat": ingestion.dataFormat,
            "fileType": ingestion.fileType,
            "sourceAddress": ingestion.sourceAddress,
            "spatialGranularity": spatialGranularity,
            "spatialScopeLevel": spatialScopeLevel,
            "temporalGranularity": temporalGranularity,
            "temporalScopeLevel": temporalScopeLevel,
            "temporalScopeStart": temporalStart,
            "temporalScopeEnd": temporalEnd,
            "theme": theme.themeDescription
        }
        metadata_list.append(metadata_entry)

        # Print Dataset summary for debugging
        print("\nConstructed Dataset:")
        print(dataset.to_dict())




    # Save metadata to the specified metadata file
    metadata_list = [dataset.to_dict() for dataset in datasets]
    with open(metadata_file, 'w', encoding='utf-8') as meta_file:
        json.dump(metadata_list, meta_file, ensure_ascii=False, indent=4)
        print(f"\nMetadata saved to {metadata_file}")







