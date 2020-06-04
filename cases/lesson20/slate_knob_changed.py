import nuke

from time import strftime
from getpass import getuser

class SlateGizmo(object):

	def __init__(self):
		self.gizmo = nuke.thisNode()

	def show_custom_slate_frame(self, knob):
		status = knob.value() == 'custom'
		self.gizmo['thumbFrame'].setVisible(status)

	def show_custom_mask(self, knob):
		status = knob.value() == 'custom'
		self.gizmo['maskPixel'].setVisible(status)

	def auto_show_name(self, knob):
		status = knob.value()
		if status:
			self.gizmo['showName'].setValue(
				self.gizmo['versionName'].value().split('_')[0].upper())
			self.gizmo['showName'].setEnabled(False)
			return
		self.gizmo['showName'].setValue('')
		self.gizmo['showName'].setEnabled(True)

	def auto_version_name(self, knob):
		status = knob.value()
		if status:
			self.gizmo['versionName'].setValue(
				os.path.splitext(os.path.basename(nuke.root().name()))[0])
			self.gizmo['versionName'].setEnabled(False)
			return
		self.gizmo['versionName'].setValue('')
		self.gizmo['versionName'].setEnabled(True)

	def change_logo_type(self, knob):
		status = knob.value() == 'icon'
		self.gizmo['logoFile'].setVisible(status)
		self.gizmo['logoScale'].setVisible(status)
		self.gizmo['logoOpacity'].setVisible(status)
		self.gizmo['logoText'].setVisible(not status)
		self.gizmo['logoColor'].setVisible(not status)


def knob_changed():
	slate = SlateGizmo()
	knob = nuke.thisKnob()
	if knob.name() == 'thumbMode':
		slate.show_custom_slate_frame(knob)
	elif knob.name() == 'autoShow':
		slate.auto_show_name(knob)
	elif knob.name() == 'autoVersion':
		slate.auto_version_name(knob)
	elif knob.name() == 'logoType':
		slate.change_logo_type(knob)
	elif knob.name() == 'maskType':
		slate.show_custom_mask(knob)
