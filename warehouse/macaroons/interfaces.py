# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from zope.interface import Interface


class IMacaroonService(Interface):
    def _extract_raw_macaroon(raw_macaroon):
        """
        Returns the base64-encoded macaroon component of a PyPI macaroon,
        dropping the prefix.

        Returns None if the macaroon is None, has no prefix, or has the
        wrong prefix.
        """

    def find_from_raw(raw_macaroon):
        """
        Returns a macaroon model from the DB from a raw macaroon, or raises
        InvalidMacaroon if not found or for malformed macaroons.
        """

    def find_macaroon(macaroon_id):
        """
        Returns a macaroon model from the DB by its identifier.
        Returns None if no macaroon has the given ID.
        """

    def find_userid(raw_macaroon):
        """
        Returns the id of the user associated with the given raw (serialized)
        macaroon.
        """

    def verify(raw_macaroon, context, principals, permission):
        """
        Returns True if the given raw (serialized) macaroon is
        valid for the context, principals, and requested permission.

        Raises InvalidMacaroon if the macaroon is not valid.
        """

    def create_macaroon(domain, user_id, description, restrictions):
        """
        Returns a tuple with:

        - the raw (serialized) macaroon string,
        - the database macaroon

        The description provided is not embedded into the macaroon, only stored in the
        DB model.
        Restrictions has the same format as in describe_caveats.
        """

    def delete_macaroon(macaroon_id):
        """
        Deletes a macaroon from the DB by its identifier.
        """

    def get_macaroon_by_description(user_id, description):
        """
        Returns a macaroon model from the DB with the given description,
        if one exists for the given user.

        Returns None if the user doesn't have a macaroon with this description.
        """

    def describe_caveats(self, caveats):
        """
        Given a value of macaroon caveats (like the one stored in DB), return a
        description of the caveats, as a dict:

        - No key: no restriction (user-wide token)
        - "projects" key: contains a list of normalized project names.
        """
