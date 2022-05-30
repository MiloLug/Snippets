from dataclasses import dataclass
from typing import Annotated, Any, Optional
import boto3




# IdentityPoolId = 'us-east-1-faskjdhajsdh4'
UserPoolId = 'eu-west-2_Ae'
ClientId = '496vvo0lf995'
region = 'eu-west-2'


class Settings:
    AWS_CLIENT_ID = ClientId


settings = Settings

UserAttributes = Annotated[dict[str, Any], 'user attributes in dict format']
CognitoUserAttributes = Annotated[list[dict[str, Any]], 'user attributes in cognito format']
Username = Annotated[str, 'username (or email)']
AuthData = Annotated[dict[str, Any], 'tokens and related data']
AccessToken = Annotated[str, 'access token']
RefreshToken = Annotated[str, 'refresh token']
ChallengeSession = Annotated[str, 'cognito challenge session']
UserSub = Annotated[str, 'cognito user uid']
ConfirmationCode = Annotated[str, 'confirmation code from the message']


# idClient = boto3.client('cognito-identity', region_name=region)
idp_client = boto3.client(
    'cognito-idp',
    region_name=region,
    aws_access_key_id='AKIA5U7U',
    aws_secret_access_key='X33lg9u0C'
)


def dict_to_cognito_attrs(data: UserAttributes) -> CognitoUserAttributes:
    return [
        {'Name': key, 'Value': value}
        for key, value in data.items()
        if value is not None
    ]

def cognito_attrs_to_dict(data: CognitoUserAttributes) -> UserAttributes:
    return {
        user_attr["Name"]: user_attr["Value"]
        for user_attr in data
    }


def sign_up_cognito_user(username: Username, phone: str, password: str, **kwargs) -> Optional[UserSub]:
    fields = {
        'phone_number': phone,
        **kwargs
    }
    response = idp_client.sign_up(
        ClientId=settings.AWS_CLIENT_ID,
        Username=username,
        Password=password,
        UserAttributes=[{'Name': key, 'Value': value} for key, value in fields.items()],
    )
    return response.get('UserSub')


def update_user(token: str, phone: str = None, **kwargs) -> Optional[list[dict]]:
    fields = {
        **kwargs
    }
    if phone:
        fields['phone_number'] = phone

    response = idp_client.update_user_attributes(
        AccessToken=token,
        UserAttributes=[{'Name': key, 'Value': value} for key, value in fields.items()],
    )

    return response


def admin_update_user(username: Username, phone: str = None, **kwargs):
    """Updates user attributes by admin. So helpful when there is no user's access token"""
    if phone:
        kwargs['phone_number'] = phone
        kwargs['phone_number_verified'] = 'true'
    if kwargs.get('email'):
        kwargs['email_verified'] = 'true'

    idp_client.admin_update_user_attributes(
        UserPoolId=UserPoolId,
        Username=username,
        UserAttributes=dict_to_cognito_attrs(kwargs),
    )


def create_cognito_user(username: str, phone: str, password: str, **kwargs):
    """
    Creates user using admin accesses
    """
    fields = {
        'email_verified': 'true',
        'email': username,
        'phone_number': phone,
        'phone_number_verified': 'true',
        **kwargs
    }
    response = idp_client.admin_create_user(
        UserPoolId=UserPoolId,
        Username=username,
        UserAttributes=[{'Name': key, 'Value': value} for key, value in fields.items()],
        TemporaryPassword=password,
        DesiredDeliveryMediums=[
            'EMAIL',
            'SMS'
        ]
    )
    user_data = response.get("User")
    return next(attr["Value"]
                for attr in user_data.get("Attributes", ()) if attr["Name"] == "sub")


def sign_in_cognito_user(username: str, password: str) -> Optional[ChallengeSession]:
    response = idp_client.initiate_auth(
        AuthFlow='USER_PASSWORD_AUTH',
        AuthParameters={
            'USERNAME': username,
            'PASSWORD': password
        },
        ClientId=ClientId
    )

    return response


def complete_cognito_sms_mfa(username: str, session: str, code: str) -> Optional[AuthData]:
    response = idp_client.respond_to_auth_challenge(
        ClientId=settings.AWS_CLIENT_ID,
        ChallengeName='SMS_MFA',
        Session=session,
        ChallengeResponses={
            'SMS_MFA_CODE': code,
            'USERNAME': username
        }
    )
    return response


def refresh_cognito_token(token: str) -> Optional[AuthData]:
    response = idp_client.initiate_auth(
        AuthFlow='REFRESH_TOKEN',
        AuthParameters={
            'REFRESH_TOKEN': token
        },
        ClientId=settings.AWS_CLIENT_ID
    )
    return response.get('AuthenticationResult')

#
# def send_password_reset_code(username: str):
#     idp_client.forgot_password(
#         Username=username,
#         ClientId=ClientId
#     )

# print(
#     sign_in_cognito_user("misticku@gmail.com", "1r")
# )
#
#
# def reset_user_password(
#         username: str,
#         code: str,
#         new_password: str):
#     idp_client.confirm_forgot_password(
#         ClientId=ClientId,
#         Username=username,
#         ConfirmationCode=code,
#         Password=new_password
#     )
#
#
# def complete_registration(username: str, tmp_password: str, new_password: str):
#     """
#     Uses a username and a password from the message to complete account creation
#         with attaching new password
#     """
#     response = idp_client.initiate_auth(
#         AuthFlow='USER_PASSWORD_AUTH',
#         AuthParameters={
#             'USERNAME': username,
#             'PASSWORD': tmp_password
#         },
#         ClientId=ClientId
#     )
#     # check the 'challenge' to be sure that we need to reset the password
#     if response.get("ChallengeName") == 'NEW_PASSWORD_REQUIRED':
#         response = idp_client.respond_to_auth_challenge(
#             ClientId=ClientId,
#             ChallengeName='NEW_PASSWORD_REQUIRED',
#             Session=response.get('Session'),
#             ChallengeResponses={
#                 'NEW_PASSWORD': new_password,
#                 'USERNAME': username
#             }
#         )
#     return response.get('AuthenticationResult')


# tmp = idp_client.admin_initiate_auth(
#     UserPoolId=UserPoolId,
#     ClientId=ClientId,
#     AuthFlow='ADMIN_NO_SRP_AUTH',
#     AuthParameters=auth_data
# )
# token = tmp['AuthenticationResult']['IdToken']
#
# tmp = idp_client.get_id(
    #     AccountId='738032',
#     IdentityPoolId=IdentityPoolId,
#     Logins={
#         f'cognito-idp.{region}.amazonaws.com/{UserPoolId}': token
#     }
# )
#
# print(tmp)

#
# # # responseponse = identity.get_cre
# credentials = idClient.get_credentials_for_identity(IdentityId=tmp["IdentityId"])['Credentials']
# access_key = credentials['AccessKeyId']
# secret_key = credentials['SecretKey']
# #
# # print(access_key)
# # print(secret_key)
#
# boto3.setup_default_session(
#     aws_access_key_id=access_key,
#     aws_secret_access_key=secret_key,
#
#     region_name='us-east-2'
# )
#
# idPoolClient = boto3.client('cognito-idp', region_name='us-east-2')
#


# response = idp_client.admin_create_user(
#     UserPoolId=UserPoolId,
#     Username='misticku@gmail.com',
#     UserAttributes=[
#         {
#             'Name': 'email_verified',
#             'Value': 'true'
#         },
#         {
#             'Name': 'email',
#             'Value': 'misticku@gmail.com'
#         },
#         {
#             'Name': 'given_name',
#             'Value': 'Michael'
#         },
#         {
#             'Name': 'family_name',
#             'Value': 'Gonchar'
#         },
#     ],
#     TemporaryPassword='12345Qwerty$',
#     # ForceAliasCreation=True|False,
#     # MessageAction='RESEND'|'SUPPRESS',
#     DesiredDeliveryMediums=[
#         'EMAIL',
#     ]
# )

# response = idp_client.admin_get_user(
#     UserPoolId=UserPoolId,
#     Username='test1@gmail.com'
# )
# #
# print(response)
#
#
# class RawUserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User,
#         fields = '__all__'
#
#
# class RetrieveUpdateUserSerializer(serializers.ModelSerializer):
#     """
#     User creation and updating base serializer
#     """
#
#     class Meta:
#         model = User
#         fields = ('id',)
#
#     def get_cognito_data(self, instance):
#         return get_cognito_user(instance.email)
#
#     def
#         @property
#         def data(self):
#             if self.instance.id:
#                 return {
#                     **RawUserSerializer(instance=self.instance).data,
#                     "cognito_profile": self.get_cognito_data(self.instance)
#                 }
#             else:
#                 return self.fields
#
#     def update(self, instance, validated_data):
#         cognito_fields = getattr(self.Meta, 'cognito_user_attributes', ())
#         cognito = {
#             name: validated_data[name]
#             for name in cognito_fields if name in validated_data
#         }
#         update_cognito_user(instance.email, **cognito)
#         return instance
#
#
# class CreateUserMixin(serializers.Serializer):
#     """
#     User creation mixin
#     """
#     email = serializers.EmailField(required=True, write_only=True)
#     password = serializers.CharField(max_length=32, required=True, write_only=True)
#
#     class Meta:
#         fields = ('email', 'password')
#         cognito_user_attributes = ()
#
#     def create(self, validated_data):
#         cognito_fields = getattr(self.Meta, 'cognito_user_attributes', ())
#         cognito = {
#             name: validated_data[name]
#             for name in cognito_fields if name in validated_data
#         }
#         cognito_user = create_cognito_user(
#             validated_data["email"],
#             validated_data["password"],
#             **cognito
#         )
#
#         return User.objects.create(username=cognito_user["Username"])
#
#
# class RetrieveUpdatePatientSerializer(UpdateUserMixin, serializers.ModelSerializer):
#     family_name = serializers.CharField(max_length=64, required=True)
#     given_name = serializers.CharField(max_length=64, required=True)
#
#     class Meta:
#         model = Patient
#         fields = ('family_name', 'given_name')
#         cognito_user_attributes = ('family_name', 'given_name')
#
#     @property
#     def data(self):
#         if self.instance.id:
#             return {
#                 'id': self.instance.id,
#                 **self.get_cognito_data(self.instance.user)
#             }
#         else:
#             return self.fields
#
#     def update(self, instance, validated_data):
#         super(RetrieveUpdatePatientSerializer, self).update(instance.user, validated_data)
#         return instance


# # SIGN IN
# # Errors: UserNotConfirmedException
# r = idp_client.initiate_auth(
#     AuthFlow='USER_PASSWORD_AUTH',
#     AuthParameters={
#         'USERNAME': 'misticku@gmail.com',
#         'PASSWORD': '12345Qty'
#     },
#     ClientId='1tf3qpart'
# )
# print(r['AuthenticationResult']['AccessToken'])

# r = idp_client.initiate_auth(
#     AuthFlow='REFRESH_TOKEN',
#     AuthParameters={
#         'REFRESH_TOKEN': 'bsdasdsad'
#     },
#     ClientId='1tf3qparc1qpvt'
# )
# print(r['AuthenticationResult']['AccessToken'])



# # SIGN UP
# # Errors: UsernameExistsException
# r = idp_client.sign_up(
#     ClientId='1tf3qpar4q5t',
#     Username='misticku@gmail.com',
#     Password='123456Qwerty',
#     UserAttributes=[
#         {
#             'Name': 'family_name',
#             'Value': 'Family'
#         },
#         {
#             'Name': 'given_name',
#             'Value': 'Given'
#         },
#         {
#             'Name': 'phone_number',
#             'Value': '+38077676'
#         },
#     ]
# )
# print(r)
# r = idp_client.admin_confirm_sign_up(
#     UserPoolId='us-east-jasgdsahjd5e',
#     Username='misticku@gmail.com'
# )
# print(r)


# CONFIRMATION
# r = idp_client.confirm_sign_up(
#     ClientId='1tf3qpav22r4q5t',
#     Username='misticku@gmail.com',
#     ConfirmationCode='525441'
# )
# print(r)
