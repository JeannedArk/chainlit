import { useRecoilValue } from 'recoil';

import AttachFile from '@mui/icons-material/AttachFile';
import { IconButton, Tooltip } from '@mui/material';

import { FileSpec, IFileResponse } from '@chainlit/components';
import { useUpload } from '@chainlit/components';

import { projectSettingsState } from 'state/project';

type Props = {
  disabled?: boolean;
  fileSpec: FileSpec;
  onFileUpload: (files: IFileResponse[]) => void;
  onFileUploadError: (error: string) => void;
};

const UploadButton = ({
  disabled,
  fileSpec,
  onFileUpload,
  onFileUploadError
}: Props) => {
  const pSettings = useRecoilValue(projectSettingsState);

  const upload = useUpload({
    spec: fileSpec,
    onResolved: (payloads: IFileResponse[]) => onFileUpload(payloads),
    onError: onFileUploadError,
    options: { noDrag: true }
  });

  if (!upload || !pSettings?.features?.multi_modal) return null;
  const { getRootProps, getInputProps, uploading } = upload;

  return (
    <Tooltip title="Upload files">
      <span>
        <input id="upload-button-input" {...getInputProps()} />
        <IconButton
          id={uploading ? 'upload-button-loading' : 'upload-button'}
          disabled={uploading || disabled}
          color="inherit"
          {...getRootProps({ className: 'dropzone' })}
        >
          <AttachFile />
        </IconButton>
      </span>
    </Tooltip>
  );
};

export default UploadButton;
