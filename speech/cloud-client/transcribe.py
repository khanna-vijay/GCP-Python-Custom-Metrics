#!/usr/bin/env python

# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Google Cloud Speech API sample application using the REST API for batch
processing.

Example usage:
    python transcribe.py resources/audio.raw
    python transcribe.py gs://cloud-samples-tests/speech/brooklyn.flac
"""

# [START import_libraries]
import argparse
import time
import io
# [END import_libraries]


def transcribe_file(speech_file, encoding, sample_rate_hertz, language):
    """Transcribe the given audio file."""
    from google.cloud import speech
    speech_client = speech.Client()

    with io.open(speech_file, 'rb') as audio_file:
        content = audio_file.read()
        audio_sample = speech_client.sample(
            content=content,
            encoding=encoding,
            sample_rate_hertz=sample_rate_hertz)

    start = time.time()
    alternatives = audio_sample.recognize(language)
    print('Runtime: %s' % (time.time() - start))
    for alternative in alternatives:
        print(u'Transcript: {}'.format(alternative.transcript))


def transcribe_gcs(gcs_uri, encoding, sample_rate_hertz, language):
    """Transcribes the audio file specified by the gcs_uri."""
    from google.cloud import speech
    speech_client = speech.Client()

    audio_sample = speech_client.sample(
        content=None,
        source_uri=gcs_uri,
        encoding=encoding,
        sample_rate_hertz=sample_rate_hertz)

    alternatives = audio_sample.recognize(language)
    for alternative in alternatives:
        print('Transcript: {}'.format(alternative.transcript))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        'path', help='File or GCS path for audio file to be recognized')
    parser.add_argument('--encoding', default='LINEAR16')
    parser.add_argument('--sample_rate', default=16000, type=int)
    parser.add_argument('--language', default='en-US')
    args = parser.parse_args()
    if args.path.startswith('gs://'):
        transcribe_gcs(args.path, args.encoding, args.sample_rate, args.language)
    else:
        transcribe_file(args.path, args.encoding, args.sample_rate, args.language)
