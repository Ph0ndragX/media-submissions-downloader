class MediaSubmissionDownloaderForReddit:

    def __init__(self, config, media_submissions):
        self._config = config
        self._media_submissions = media_submissions
        self._num_to_download = 0

    def run(self):
        print('[+] User: {}'.format(self._media_submissions.user().name))
        print('[+] Loaded {} submissions.'.format(len(self._media_submissions.submissions())))

        if self._config.display():
            self._display_submissions()
        else:
            self._download_submissions()

    def _display_submissions(self):
        print('[+] Listing saved submissions.')
        submissions = self._media_submissions.submissions()
        for idx, submission in enumerate(submissions):
            print(MediaSubmissionDownloaderForReddit._format_submission_display(
                len(submissions),
                idx,
                submission
            ))

    def _download_submissions(self):
        print('[+] Submissions will be saved to: {}'.format(self._config.save_dir()))

        downloaded_submissions = self._media_submissions.downloaded_submissions()
        if len(downloaded_submissions) > 0:
            print('[+] There are already {} submissions downloaded, these will be omitted.'
                  .format(len(downloaded_submissions)))

        print('[+] Starting submissions download.')

        self._num_to_download = len(self._media_submissions.submissions()) - len(downloaded_submissions)

        print('[+] {} submissions will be downloaded.'.format(self._num_to_download))

        self._media_submissions.save(
            lambda idx, sub: self._on_submission_downloaded(idx, sub),
            lambda idx, sub, e: self._on_submission_download_error(idx, sub, e)
        )

    def _on_submission_downloaded(self, idx, submission):
        print(MediaSubmissionDownloaderForReddit._format_submission_display(
            self._num_to_download,
            idx,
            submission,
            "Downloaded"
        ), flush=True)

    def _on_submission_download_error(self, idx, submission, exception):
        print(MediaSubmissionDownloaderForReddit._format_submission_display(
            self._num_to_download,
            idx,
            submission,
            f"Saving error: {exception}"
        ), flush=True)

    @staticmethod
    def _format_submission_display(max_idx, idx, submission, message=''):
        max_idx_width = str(len(str(max_idx)))
        fmt = "[{:^" + max_idx_width + "}/{}] {:<32.32} | {:^23}"
        title = submission.title() if len(submission.title()) <= 32 else submission.title()[:(32 - 3)] + '...'
        formatted = fmt.format(idx, max_idx, title, submission.shortlink())
        return formatted if message == '' else formatted + ' | ' + message
